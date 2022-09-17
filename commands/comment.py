import sublime, sublime_plugin

def shift_region(region, shift):
    return sublime.Region(region.a + shift, region.b + shift)

def advance_to_first_non_white_space_on_line(view, pt):
    while True:
        c = view.substr(sublime.Region(pt, pt + 1))
        if c == " " or c == "\t":
            pt += 1
        else:
            break

    return pt

def has_non_white_space_on_line(view, pt):
    while True:
        c = view.substr(sublime.Region(pt, pt + 1))
        if c == " " or c == "\t":
            pt += 1
        else:
            return c != "\n"

def build_comment_data(view, pt):
    shell_vars = view.meta_info("shellVariables", pt)
    if not shell_vars:
        return ([], [])

    # transform the list of dicts into a single dict
    all_vars = {}
    for v in shell_vars:
        if 'name' in v and 'value' in v:
            all_vars[v['name']] = v['value']

    line_comments = []
    block_comments = []

    # transform the dict into a single array of valid comments
    suffixes = [""] + ["_" + str(i) for i in range(1, 10)]
    for suffix in suffixes:
        start = all_vars.setdefault("TM_COMMENT_START" + suffix)
        end = all_vars.setdefault("TM_COMMENT_END" + suffix)
        mode = all_vars.setdefault("TM_COMMENT_MODE" + suffix)
        disable_indent = all_vars.setdefault("TM_COMMENT_DISABLE_INDENT" + suffix)

        if start and end:
            start = start.replace('\\n', '\n')
            end = end.replace('\\n', '\n')
            block_comments.append((start, end, disable_indent == 'yes'))
            block_comments.append((start.strip(), end.strip(), disable_indent == 'yes'))
        elif start:
            line_comments.append((start, disable_indent == 'yes'))
            line_comments.append((start.strip(), disable_indent == 'yes'))

    return (line_comments, block_comments)

class ToggleCommentDjangoCommand(sublime_plugin.TextCommand):

    def remove_block_comment(self, view, edit, comment_data, region):
        (line_comments, block_comments) = comment_data

        # Call extract_scope from the midpoint of the region, as calling it
        # from the start can give false results if the block comment begin/end
        # markers are assigned their own scope, as is done in HTML.
        whole_region = view.extract_scope(region.begin() + region.size() / 2)

        for c in block_comments:
            (start, end, disable_indent) = c
            start_region = sublime.Region(whole_region.begin(),
                whole_region.begin() + len(start))
            end_region = sublime.Region(whole_region.end() - len(end),
                whole_region.end())

            if view.substr(start_region) == start and view.substr(end_region) == end:

                # erase whole line of block comment if it's the only thing on the line
                if start_region.begin() == view.line(start_region).begin() and start_region.end() == view.line(start_region).end():
                    start_region.a -= 1
                if end_region.begin() == view.line(end_region).begin() and end_region.end() == view.line(end_region).end():
                    end_region.a -= 1
                # It's faster to erase the start region first
                view.erase(edit, start_region)

                end_region = sublime.Region(
                    end_region.begin() - start_region.size(),
                    end_region.end() - start_region.size())

                view.erase(edit, end_region)
                return True

        return False


    def block_comment_region(self, view, edit, block_comment_data, region):
        (start, end, disable_indent) = block_comment_data

        if region.empty():
            # Silly buggers to ensure the cursor doesn't end up after the end
            # comment token
            view.replace(edit, sublime.Region(region.end()), 'x')
            view.insert(edit, region.end() + 1, end)
            view.replace(edit, sublime.Region(region.end(), region.end() + 1), '')
            view.insert(edit, region.begin(), start)
        else:
            view.insert(edit, region.end(), end)
            view.insert(edit, region.begin(), start)

        view.selection.clear()
        view.selection.add(shift_region(region, len(start)))

    def add_comment(self, view, edit, comment_data, prefer_block, region):
        (line_comments, block_comments) = comment_data

        if len(line_comments) == 0 and len(block_comments) == 0:
            return

        comment_block_style = block_comments[0]
        if len(block_comments) >= 2:
            comment_block_style = block_comments[2]

        lines = view.lines(region)


        comment_style = prefer_block and comment_block_style or block_comments[0]


        if len(lines) <= 1 and not has_non_white_space_on_line(view, region.begin()):
            # If nothing on line
            self.block_comment_region(view, edit, comment_style, region)

        elif len(lines) <= 1:
            # If selection ends on the beginning of the next line,
            # move the comment surrounder to the end of the previous line.
            endpos = view.rowcol(region.end())
            if endpos[1] == 0:
                region.b = region.b - 1

            self.block_comment_region(view, edit, comment_style, region)
        else:
            # For multi-line (true block) comments -- {% comment %}
            # if region ends at the end of a line, bump to the next line
            if region.end() == view.line(region).end():
                region.b = region.b + 1

            startpos = view.rowcol(region.begin())
            endpos = view.rowcol(region.end())

            comment_style = list(comment_block_style)
            if startpos[1] == 0:
                comment_style[0] += "\n"
            if endpos[1] == 0:
                comment_style[1] += "\n"


            self.block_comment_region(view, edit, comment_style, region)

    def run(self, edit, block=False):
        for region in self.view.sel():
            comment_data = build_comment_data(self.view, region.begin())
            if (region.end() != self.view.size() and
                    build_comment_data(self.view, region.end()) != comment_data):
                # region spans languages, nothing we can do
                continue

            if self.remove_block_comment(self.view, edit, comment_data, region):
                continue

            has_line_comment = len(comment_data[0]) > 0
            if not has_line_comment and not block and region.empty():
                # Use block comments to comment out the line
                line = self.view.line(region.a)
                line = sublime.Region(
                    advance_to_first_non_white_space_on_line(self.view, line.a),
                    line.b)

                # Try and remove any existing block comment now
                if self.remove_block_comment(self.view, edit, comment_data, line):
                    continue

                self.add_comment(self.view, edit, comment_data, block, line)
                continue

            # Add a comment instead
            self.add_comment(self.view, edit, comment_data, block, region)
