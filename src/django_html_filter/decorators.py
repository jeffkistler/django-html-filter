"""
Useful decorators for views.
"""
from functools import wraps

from django.utils.decorators import available_attrs

from django_html_filter.middleware import HTMLFilterMiddleware
from django_html_filter.conf import settings

def html_filter_exempt(view):
    """
    Marks a view as being exempt from response filtering.
    """
    def wrapped_view(request, *args, **kwargs):
        setattr(request, settings.EXEMPT_FLAG, True)
        return view(request, *args, **kwargs)
    return wraps(view, assigned=available_attrs(view))(wrapped_view)

def html_filter(**middleware_kwargs):
    """
    Filter the response HTML from a view.
    """
    middleware = HTMLFilterMiddleware(**middleware_kwargs)
    def decorator(view):
        def wrapped_view(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            new_response = middleware.process_response(request, response)
            return new_response
        return wraps(view, assigned=available_attrs(view))(wrapped_view)
    return decorator
