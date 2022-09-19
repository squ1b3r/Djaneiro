import sublime, sublime_plugin

from pathlib import Path
from glob import iglob
import json
import subprocess

class URLIndex:
    def __init__(self, *args, **kwargs):
        self.autocomplete = []
        self.index = {}

    @classmethod
    def init_with_index(cls, index):
        self = cls()
        self.autocomplete = {i[2]: i for i in index if i[2] is not None}
        self.index = index
        return self

class DjangoUrlsIndexer(sublime_plugin.WindowCommand):
    """A window command to index django url files."""


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_running = False

        # urls.py path to url names
        self.window_index = {}
        self.python_interpreter = None


    def run(self):
        """Runs the indexer command.
        Once this starts running, it will not listen to other calls until the
        index is finished running.
        """
        print("DJI RUN")
        if self._is_running:
            return
        self._is_running = True
        self.window.active_view().set_status('DjangoUrls index', 'starting')
        self._total_indexed = 0
        print("Index start")
        return ["a"]

    def clear_index(self):
        self.index = {}

    def set_window_index(self, window, index):
        self.window_index[window] = URLIndex.init_with_index(index)

    def index_project_folders(self, window, project_folders):
        print(project_folders)
        managepy = None
        for folder in project_folders:
            path = Path(folder.get('path'))
            exclude = folder.get('folder_exclude_patterns')
            managepy = path.glob('**/manage.py')
            if not managepy:
                continue

        if not managepy:
            print("No Manage.py found.")
            return
        managepy = next(managepy)
        print(managepy)

        this_path = Path( __file__ ).parent.absolute()
        cmd = f'import sys; sys.path.append("{this_path}"); from url_extract import run; run()'
        result = subprocess.run([self.python_interpreter, managepy, "shell", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stderr)
        if not result.stdout:
            return

        self.set_window_index(window, json.loads(result.stdout))

    def get_index_for_window(self, window):
        return self.window_index.get(window)

djurls_indexer = DjangoUrlsIndexer(sublime.active_window())


class DjangoUrlsPlugin(sublime_plugin.EventListener):
    def on_activated(self, view):
        #return
        # for testing
        self.on_load_project_async(view.window())

    def on_load_project_async(self, window):
        print("on load")
        project_data = window.project_data()

        print(window, "just got loaded", project_data)
        python_interpreter = project_data.get('settings', {}).get('python_interpreter')
        project_folders = project_data.get('folders')
        if not project_folders or not python_interpreter:
            return
        djurls_indexer.python_interpreter = Path(python_interpreter)
        djurls_indexer.index_project_folders(window, project_folders)

        # Call Indexer if view doesn't have a url index
        #if not hasattr(view, "djurlindex"):
        #    view.djurlindex = djurls_indexer.run()
        #    print("index updated")

    def on_query_completions(self, view, prefix, locations):
        print("qc11")
        if not view.match_selector(locations[0], "text.url-name.django"):
            return []

        print("qc", view.window(), dir(view.window()))

        index = djurls_indexer.get_index_for_window(view.window())
        if not index:
            return

        print(index, prefix)
        prefix = prefix.lower()
        print(index.autocomplete)
        out = []
        for view_name, payload in index.autocomplete.items():
            if view_name.lower().startswith(prefix):
                params = ''
                if payload[3]:
                    params = " " + " ".join([f'${{{i}:{p}}}' for i, p in enumerate(payload[3], 1)])
                print(params)
                out.append((
                f'{view_name}\t{payload[0]}', f"'{view_name}'" + params
            ))
        print(out)

        return (out, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

#     def on_pre_save(self, view):
#         print(view.file_name(), "is about to be saved")

#     def on_post_save(self, view):
#         print(view.file_name(), "just got saved")

#     def on_new(self, view):
#         print("new file")

#     def on_modified(self, view):
#         print(view.file_name(), "modified")

#     def on_activated(self, view):
#         print(view.file_name(), "is now the active view")

#     def on_close(self, view):
#         print(view.file_name(), "is no more")

#     def on_clone(self, view):
#         print(view.file_name(), "just got cloned")
