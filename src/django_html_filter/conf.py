from django.conf import settings as project_settings
from django_html_filter import defaults

class AppSettings(object):
    """
    An app-level settings container.

    """
    def __init__(self, defaults, overrides, prefix=None):
        self.defaults = defaults
        self.overrides = overrides
        if prefix:
            self.prefix = prefix + '_'
        else:
            self.prefix = ''
        
    def __getattr__(self, name):
        val = getattr(self.overrides,
                      self.prefix + name,
                      getattr(self.defaults, name))
        if callable(val):
            val = val()
        return val

settings = AppSettings(defaults, project_settings, 'HTML_FILTER')
