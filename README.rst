django-html-filter
==================

Filter HTML output from Django views.

django-html-filter uses html5lib_ to parse the response content and then filter the resulting parse tree to transform the resulting markup in various useful ways, such as dropping unnecessary tags, dropping unnecessary quotes and removing insignificant whitespace.

.. _html5lib: http://code.google.com/p/html5lib/

Installation
------------

Installation from Source
````````````````````````

Unpack the archive, ``cd`` to the source directory, and run the following command::

    python setup.py install

Installation with pip and git
`````````````````````````````

Assuming you have pip and git installed, run the following command to install from the GitHub repository::

    pip install git+git://github.com/jeffkistler/django-html-filter.git#egg=django-html-filter

Usage
-----

Middleware
``````````

The middleware will filter all HTML responses with an HTML ``Content-Type`` header and a ``200 - OK`` status code. To enable it, add ``django_html_filter.middleware.HTMLFilterMiddleware`` to your project's ``MIDDLEWARE_CLASSES`` setting like so::

    MIDDLEWARE_CLASSES = (
        'django.middleware.gzip.GZipMiddleware',
        'django_html_filter.middleware.HTMLFilterMiddleware',
        ...
    )

Note that this middleware should come before any response middleware that alters response content, but after middleware that alters the content encoding, such as the GZip middleware.

To disable the middleware for a specific view, use the included ``html_filter_exempt`` decorator:

    from django_html_filter.decorators import html_filter_exempt

    @html_filter_exempt
    def my_view(request):
        ...


Decorator
`````````

If you'd like a more fine-grained approach to filtering responses, the ``html_filter`` decorator enables you to apply filtering to responses explicitly:

    from django_html_filter.decorators import html_filter

    @html_filter()
    def my_view(request):
        ...

You can even pass options to the ``html_filter`` decorator to customize the filtering for a specific view:

    @html_filter(strip_whitespace=True)
    def my_view(request):
        ...

Note that the options must be lower-case keyword arguments corresponding to the upper-case settings described below stripped of the ``HTML_FILTER_`` prefix.

Settings
````````

Described here are the settings for customizing how filters are applied to responses.

``HTML_FILTER_ENABLED``
    A boolean controlling whether or not response filtering will occur for both the middleware and decorators. Defaults to ``True``.

``HTML_FILTER_QUOTE_ATTR_VALUES``
    A boolean controlling whether or not attribute values are quoted. Defaults to ``False``.

``HTML_FILTER_QUOTE_CHAR``
    Should be a quote character. Defaults to ``'"'``.

``HTML_FILTER_USE_BEST_QUOTE_CHAR``
    A boolean controlling whether the filter should choose the best quote character or not. Defaults to ``True``.

``HTML_FILTER_OMIT_OPTIONAL_TAGS``
    A boolean controlling whether the filter should drop optional HTML tags at render time. Defaults to ``True``.

``HTML_FILTER_MINIMIZE_BOOLEAN_ATTRIBUTES``
    A boolean controlling whether or not the filter will leave boolean attribute values intact or discard them. Defaults to ``True``.

``HTML_FILTER_USE_TRAILING_SOLIDUS``
    A boolean controlling whether or not the filter will insert a close-tag slash at the end of the start tag of void elements. Defaults to ``False``.

``HTML_FILTER_SPACE_BEFORE_TRAILING_SOLIDUS``
    A boolean controlling whether or not the filter will insert a space before the close-tag slash at the end of a start tag of void elements. Defaults to ``True``.

``HTML_FILTER_ESCAPE_LT_IN_ATTRS``
    A boolean controlling whether to escape ``'<'`` in attribute values. Defaults to ``False``.

``HTML_FILTER_ESCAPE_RCDATA``
    A boolean controlling whether to escape characters that need to be escaped within normal elements within rcdata elements such as 'style'. Defaults to ``False``.

``HTML_FILTER_RESOLVE_ENTITIES``
    A boolean controlling whether to resolve named character entities that appear in the source tree. The XML predefined entities &lt; &gt; &amp; &quot; &apos; are unaffected by this setting. Defaults to ``True``.

``HTML_FILTER_INJECT_META_CHARSET``
    A boolean controlling whether to insert a meta element to define the character set of the document. Defaults to ``True``.

``HTML_FILTER_STRIP_WHITESPACE``
    A boolean controlling whether to remove semantically meaningless whitespace. This compresses all whitespace to a single space except within pre. Defaults to ``False``.
