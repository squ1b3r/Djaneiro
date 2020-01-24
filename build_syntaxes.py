#!/usr/bin/python3
"""
Re-generates CSS and XML syntax definitions from the HTML one.
"""
if __name__ == '__main__':
    import os, sys
    check = sys.argv[1:] == ['check']

    ORIGINAL = (
        'HTML',
        'html, djt, html.djt, dj.html, djhtml',
        'text.html.django',
    )

    VARIATIONS = [(
        'CSS',
        'css, css.djt, dj.css, djcss',
        'source.css.django',
    ), (
        'XML',
        'xml, xml.djt, dj.xml, djxml',
        'text.xml.django',
    )]

    NAME_PATTERN = '{} (Django)'

    def fp(variation):
        name = NAME_PATTERN.format(variation) + '.sublime-syntax'
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Syntaxes', name)

    def replace(haystack, format_string, needle, replacement):
        needle = format_string.format(needle)
        assert needle in haystack
        return haystack.replace(needle, format_string.format(replacement))

    orig_name, orig_ext, orig_scope = ORIGINAL
    s = open(fp(orig_name)).read()

    for variation, extensions, scope in VARIATIONS:
        sv = replace(s, 'name: ' + NAME_PATTERN, orig_name, variation)
        sv = replace(sv, '[{}]', orig_ext, extensions)
        sv = replace(sv, '{}', orig_scope, scope)
        sv = replace(sv, 'Packages/{0}/{0}.sublime-syntax', orig_name, variation)
        n = fp(variation)
        if check:
            assert open(n, 'r').read() == sv, "build.py detected difference between HTML and {} sublime-syntax files".format(variation)
            print('Checked:', n)
        else:
            with open(n, 'w') as f:
                f.write(sv)
            print('Saved:', n)
