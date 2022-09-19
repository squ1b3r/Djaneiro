from django.urls import get_resolver, URLPattern, URLResolver  # type: ignore

import json

def describe_pattern(p):
    return str(p.pattern)

def extract_views_from_urlpatterns(urlpatterns, base='', namespace=None):
    """
    Return a list of views from a list of urlpatterns.

    Each object in the returned list is a three-tuple: (view_func, regex, name)
    """
    views = []
    for p in urlpatterns:
        if isinstance(p, (URLPattern)):
            try:
                if not p.name:
                    name = p.name
                elif namespace:
                    name = '{0}:{1}'.format(namespace, p.name)
                else:
                    name = p.name
                pattern = describe_pattern(p)
                views.append((p.callback, base + pattern, name, p.pattern.converters.keys()))
            except ViewDoesNotExist:
                continue
        elif isinstance(p, (URLResolver)):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            if namespace and p.namespace:
                _namespace = '{0}:{1}'.format(namespace, p.namespace)
            else:
                _namespace = (p.namespace or namespace)
            pattern = describe_pattern(p)
            views.extend(extract_views_from_urlpatterns(patterns, base + pattern, namespace=_namespace))
        elif hasattr(p, '_get_callback'):
            try:
                views.append((p._get_callback(), base + describe_pattern(p), p.name, p.pattern.converters.keys()))
            except ViewDoesNotExist:
                continue
        elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(patterns, base + describe_pattern(p), namespace=namespace))
        else:
            raise TypeError("%s does not appear to be a urlpattern object" % p)
    return views

def run():
    views = extract_views_from_urlpatterns(get_resolver().url_patterns)
    output = [(f'{view[0].__module__}.{view[0].__name__}', view[1], view[2], list(view[3])) for view in views]
    print(json.dumps(output))
