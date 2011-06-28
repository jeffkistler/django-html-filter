"""
The core functionality of the application, contained in the middleware.
"""
from django.http import HttpResponse
from django.conf import settings as project_settings

from html5lib import (
    html5parser, treebuilders, treewalkers
)
from html5lib.serializer import htmlserializer

from django_html_filter.conf import settings
from django_html_filter.utils import parse_content_type, parse_subtype


SERIALIZER_OPTIONS = ('quote_attr_values', 'quote_char', 'use_best_quote_char',
          'minimize_boolean_attributes', 'use_trailing_solidus',
          'space_before_trailing_solidus', 'omit_optional_tags',
          'strip_whitespace', 'inject_meta_charset', 'escape_lt_in_attrs',
          'escape_rcdata', 'resolve_entities')
KNOWN_TYPES = ('html',)

def get_global_serializer_options():
    """
    Get the settings options for the HTML serializer.
    """
    options = {}
    for option in SERIALIZER_OPTIONS:
        options[option] = getattr(settings, option.upper())
    return options

class HTMLFilterMiddleware(object):
    """
    A middleware to apply various filters to HTML responses, such as omitting
    unnecessary tags, stripping insignificant whitespace, etc.
    """
    def __init__(self, **options):
        self.options = options

    def get_allowed_types(self):
        return self.options.get('allowed_types', settings.ALLOWED_TYPES)

    def get_serializer_options(self):
        options = get_global_serializer_options()
        options.update(self.options)
        return options

    def filter_response(self, response, encoding=None):
        """
        Filter and fix-up the response object.
        """
        # Parse the response
        tree_type = settings.TREE_TYPE
        # Here we check for a TemplateResponse in the case we're being
        # used as a view decorator.
        if hasattr(response, 'render') and callable(response.render):
            response.render()
        tree = html5parser.parse(
            response.content, treebuilder=tree_type, encoding=encoding
        )
        # Build the serializer
        walker = treewalkers.getTreeWalker(tree_type)
        stream = walker(tree)
        options = self.get_serializer_options()
        serializer = htmlserializer.HTMLSerializer(**options)
        output = serializer.render(stream)
        output = output.encode(encoding)
        # Fix up the response
        response.content = output
        response['Content-Length'] = str(len(output))
        # Add a flag to prevent further filtering if the decorator is already
        # used on this response.
        setattr(response, settings.FILTERED_FLAG, True)
        return response

    def should_filter(self, request, response, content_type):
        """
        Should we parse and filter the response content?
        """
        if response.status_code != 200:
            return False
        elif content_type not in self.get_allowed_types():
            return False
        elif getattr(request, settings.EXEMPT_FLAG, False):
            return False
        elif getattr(response, settings.FILTERED_FLAG, False):
            return False
        elif parse_subtype(content_type) not in KNOWN_TYPES:
            return False
        elif response.get('Content-Encoding', 'identity') != 'identity':
            return False
        return True

    def process_response(self, request, response):
        if settings.ENABLED:
            content_type, params = parse_content_type(response['Content-Type'])
            if self.should_filter(request, response, content_type):
                charset = params.get('charset', project_settings.DEFAULT_CHARSET)
                response = self.filter_response(response, charset)
        return response
