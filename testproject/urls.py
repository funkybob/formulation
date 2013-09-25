try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


def dummy_view(request, *args, **kwargs):
    return 'dummy'


urlpatterns = patterns('',
    url(r'^$', dummy_view),
)
