from django.conf.urls.defaults import *
from django.template.response import TemplateResponse

from django_html_filter import decorators

def index(request):
    return TemplateResponse(request, 'blog-html5.html')

def other_index(request):
    return index(request)

def last_index(request):
    return index(request)

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^exempt/$', decorators.html_filter_exempt(other_index)),
    url(r'^decorator/$', decorators.html_filter(strip_whitespace=True)(last_index)),
)
