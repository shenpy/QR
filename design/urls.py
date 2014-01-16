from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import IndexView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^user/', include('users.urls')),
    url(r'^question/', include('questions.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
