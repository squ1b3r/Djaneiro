import sublime, sublime_plugin

from collections import namedtuple
from pathlib import Path
from glob import iglob
import json
import subprocess

from .utils.common import Logger

logger = Logger(__name__)

IndexEntry = namedtuple("IndexEntry", ["full_method", "url", "method_name", "kwargs"])


class URLIndex(dict):
    @classmethod
    def init_with_index(cls, index):
        self = cls()
        self = {i[2].lower(): IndexEntry(*i) for i in index if i[2] is not None}
        return self


class DjangoUrlsIndexer(sublime_plugin.WindowCommand):
    """A window command to index django url files."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_running = False

        # urls.py path to url names
        self.window_index = {}
        self.python_interpreter = None

    def clear_index(self):
        self.index = {}

    def set_window_index(self, window, index):
        self.window_index[window] = URLIndex.init_with_index(index)

    def index_project_folders(self, window, project_folders):
        if self._is_running:
            return
        self._is_running = True

        logger.debug("Indexing project data...")
        managepy = None
        for folder in project_folders:
            path_str = folder.get("path")
            if not path_str:
                continue
            path = Path(path_str)
            exclude = folder.get("folder_exclude_patterns")
            managepy = path.glob("**/manage.py")
            if not managepy:
                continue

        if not managepy:
            logger.info("No manage.py found in project.  URL Index stopped.")
            return

        managepy = next(managepy)

        this_path = Path(__file__).parent.absolute() / "utils"
        cmd = f'import sys; sys.path.append("{this_path}"); from url_extract import run; run()'
        result = subprocess.run(
            [self.python_interpreter, managepy, "shell", "-c", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.stderr:
            logger.error(result.stderr)

        if not result.stdout:
            logger.warning("No output from url_extract script.")
            return

        self.set_window_index(window, json.loads(result.stdout))

        logger.debug("Indexing complete.")

        self._is_running = False

    def get_index_for_window(self, window):
        return self.window_index.get(window)


djurls_indexer = DjangoUrlsIndexer(sublime.active_window())


class DjangoUrlsPlugin(sublime_plugin.EventListener):
    # def on_activated(self, view):
    #     # for testing
    #     self.on_load_project_async(view.window())

    def on_load_project_async(self, window):
        project_data = window.project_data()

        if not project_data:
            return

        window.active_view().set_status(
            "djaneiro", "Reloading URL index for Djaneiro..."
        )

        python_interpreter = project_data.get("settings", {}).get("python_interpreter")
        project_folders = project_data.get("folders")

        if not project_folders or not python_interpreter:
            return

        djurls_indexer.python_interpreter = Path(python_interpreter)
        djurls_indexer.index_project_folders(window, project_folders)
        window.active_view().erase_status("djaneiro")

    def on_query_completions(self, view, prefix, locations):
        format_method = None

        if view.match_selector(locations[0], "meta.function_call.python"):
            LENGTH_OF_REVERSE = len(prefix) + 8
            region = sublime.Region(
                locations[0] - LENGTH_OF_REVERSE, locations[0] - len(prefix)
            )
            if view.substr(region) == "reverse(":
                format_method = self.completions_for_reverse

        elif view.match_selector(locations[0], "text.url-name.django"):
            format_method = self.completions_for_url_tag

        if not format_method:
            return []

        index = djurls_indexer.get_index_for_window(view.window())
        if not index:
            return []

        prefix = prefix.lower()

        out = []
        for view_name, index_entry in index.items():
            if view_name.startswith(prefix):
                out.append(format_method(index_entry))

        return (
            out,
            sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS,
        )

    def completions_for_reverse(self, index_entry):

        params = ""
        if index_entry.kwargs:
            params = ", ".join(
                [f"'{p}': ${{{i}:{p}}}" for i, p in enumerate(index_entry.kwargs, 1)]
            )
            params = ", kwargs={" + params + "}"

        return (
            f"{index_entry.method_name}\t{index_entry.full_method}",
            f"'{index_entry.method_name}'{params}",
        )

    def completions_for_url_tag(self, index_entry):
        params = ""
        if index_entry.kwargs:
            params = " " + " ".join(
                [f"${{{i}:{p}}}" for i, p in enumerate(index_entry.kwargs, 1)]
            )
        return (
            f"{index_entry.method_name}\t{index_entry.full_method}",
            f"'{index_entry.method_name}'{params}",
        )

    def on_post_save(self, view):
        if not view.match_selector(0, "source.python"):
            return

        # look for the variable urlpatterns
        if view.find("urlpatterns", 0).empty():
            return

        self.on_load_project_async(view.window())
