from django import test
from django.conf import settings
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.core.urlresolvers import clear_url_caches

DEFAULTS = {
    'ENABLED': True,
    'TREE_TYPE': 'dom',
    'ALLOWED_TYPES': ('text/html',),
    'EXEMPT_FLAG': 'html_filter_exempt',
    'FILTERED_FLAG': 'html_filter_applied',
    'QUOTE_ATTR_VALUES': False,
    'QUOTE_CHAR': u'"',
    'USE_BEST_QUOTE_CHAR': True,
    'OMIT_OPTIONAL_TAGS': True,
    'MINIMIZE_BOOLEAN_ATTRIBUTES': True,
    'USE_TRAILING_SOLIDUS': False,
    'SPACE_BEFORE_TRAILING_SOLIDUS': True,
    'ESCAPE_LT_IN_ATTRS': False,
    'ESCAPE_RCDATA': False,
    'RESOLVE_ENTITIES': True,
    'INJECT_META_CHARSET': True,
    'STRIP_WHITESPACE': False,
}

TEST_MIDDLEWARE = (
    'django.middleware.gzip.GZipMiddleware',
    'django_html_filter.middleware.HTMLFilterMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEST_MIDDLEWARE_DISABLED = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

html = """<html>
  <head>
    <title>Test</title>
  </head>
  <body id="body">
    <h1>Test</h1>
  </body>
</html>
"""

html_404 = """<html>
  <head>
    <title>Not Found</title>
  </head>
  <body>
    <h1>Not Found</h1>
  </body>
</html>
"""

def test_view(request):
    return HttpResponse(html)

def test_404(request):
    return HttpResponse(html_404, status=404)

urlpatterns = patterns('',
    url(r'^$', test_view, name='test_view'),
    url(r'^404/$', test_404, name='test_404'),
)
    
class NotSet(object):
    pass
not_set = NotSet()

class BaseTestCase(test.TestCase):
    """
    Lets us patch settings.
    """
    urls = 'django_html_filter.tests'

    def setUp(self):
        self._patched_settings = {}

    def tearDown(self):
        self.unpatchSettings()

    def patchSettings(self, **kwargs):
        to_patch = DEFAULTS.copy()
        to_patch.update(kwargs)
        for key, value in to_patch.items():
            key = 'HTML_FILTER_%s' % key
            old_value = getattr(settings, key, not_set)
            self._patched_settings[key] = old_value
            setattr(settings, key, value)

    def unpatchSettings(self):
        for key, value in self._patched_settings.items():
            if value is not_set:
                delattr(settings, key)
            else:
                setattr(settings, key, value)


class MiddlewareTestCase(BaseTestCase):
    def setUp(self):
        super(MiddlewareTestCase, self).setUp()
        self._old_middleware = settings.MIDDLEWARE_CLASSES
        settings.MIDDLEWARE_CLASSES = TEST_MIDDLEWARE

    def tearDown(self):
        super(MiddlewareTestCase, self).setUp()
        settings.MIDDLEWARE_CLASSES = self._old_middleware

    def testNoFilter(self):
        self.patchSettings(ENABLED=False)
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)
        self.assertEquals(html, response.content)

    def testFilter(self):
        self.patchSettings(
            QUOTE_ATTR_VALUES=False,
            OMIT_OPTIONAL_TAGS=True
        )
        response = self.client.get('/')
        # Test that the 'id' attribute is not quoted
        self.assertNotEquals(html, response.content)
        self.assertContains(response, 'id=body')
        # Are unnecessary tags stripped?
        self.assertNotContains(response, '</body>')

    def testFilterStripWhitespace(self):
        # Test that config options are applied
        self.patchSettings(STRIP_WHITESPACE=True)
        response = self.client.get('/')
        self.assertNotEquals(html, response.content)
        self.assertContains(response, '> <')

    def testFilterBadStatusCode(self):
        response = self.client.get('/404/')
        self.assertEquals(html_404, response.content)


class DecoratorsTestCase(BaseTestCase):
    def setUpURLs(self):
        from django_html_filter.decorators import html_filter, html_filter_exempt
        settings.ROOT_URLCONF = patterns('',
            url(r'^$', test_view, name='test_view'),
            url(r'^exempt/$', html_filter_exempt(test_view), name='exempt'),
            url(r'^filtered/$', html_filter()(test_view), name='filtered'),
            url(r'^args/$', html_filter(strip_whitespace=True)(test_view), name='args'))
        clear_url_caches()

    def testFilterExempt(self):
        self.setUpURLs()
        self.patchSettings(ENABLED=True)
        old_middleware = settings.MIDDLEWARE_CLASSES
        settings.MIDDLEWARE_CLASSES = TEST_MIDDLEWARE
        response = self.client.get('/exempt/')
        self.assertContains(response, html)
        settings.MIDDLEWARE_CLASSES = old_middleware

    def testFilter(self):
        self.setUpURLs()
        self.patchSettings(ENABLED=True)
        old_middleware = settings.MIDDLEWARE_CLASSES
        settings.MIDDLEWARE_CLASSES = TEST_MIDDLEWARE_DISABLED
        response = self.client.get('/filtered/')
        self.assertNotEquals(html, response.content)
        self.assertNotContains(response, '</body>')
        settings.MIDDLEWARE_CLASSES = old_middleware

    def testFilterTwice(self):
        self.setUpURLs()
        self.patchSettings(ENABLED=True)
        old_middleware = settings.MIDDLEWARE_CLASSES
        settings.MIDDLEWARE_CLASSES = TEST_MIDDLEWARE
        once = self.client.get('/')
        twice = self.client.get('/filtered/')
        self.assertEquals(once.content, twice.content)
        settings.MIDDLEWARE_CLASSES = old_middleware

    def testFilterArgs(self):
        self.setUpURLs()
        from django.core.urlresolvers import resolve
        self.patchSettings(ENABLED=True, STRIP_WHITESPACE=False)
        old_middleware = settings.MIDDLEWARE_CLASSES
        settings.MIDDLEWARE_CLASSES = TEST_MIDDLEWARE
        once = self.client.get('/')
        twice = self.client.get('/args/')
        self.assertNotEquals(once.content, twice.content)
        self.assertContains(twice, '> <')
        settings.MIDDLEWARE_CLASSES = old_middleware
