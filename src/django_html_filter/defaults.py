"""
Defaults for application settings.
"""
# Middleware defaults
ENABLED = True
TREE_TYPE = 'dom'
ALLOWED_TYPES = ('text/html',)
EXEMPT_FLAG = 'html_filter_exempt'
FILTERED_FLAG = 'html_filter_applied'

# Serializer defaults
QUOTE_ATTR_VALUES = False
QUOTE_CHAR = u'"'
USE_BEST_QUOTE_CHAR = True
OMIT_OPTIONAL_TAGS = True
MINIMIZE_BOOLEAN_ATTRIBUTES = True
USE_TRAILING_SOLIDUS = False
SPACE_BEFORE_TRAILING_SOLIDUS = True
ESCAPE_LT_IN_ATTRS = False
ESCAPE_RCDATA = False
RESOLVE_ENTITIES = True
INJECT_META_CHARSET = True
STRIP_WHITESPACE = False
