from django.conf.urls import patterns, include, url
from .views import IndexView
from notifications.views import NotificationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^user/', include('users.urls')),
    url(r'^question/', include('questions.urls')),
    url(r'^notifications/', NotificationView.as_view(), name='design-notification'),
    url(r'^admin/', include(admin.site.urls)),
)
