# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from users.views import UserHomeView, LoginView, LogoutView, SignupView, \
                            UserView


urlpatterns = patterns('',
    url(r'^home/$', UserHomeView(), name='users-user_home'),
    url(r'^signup/$', SignupView.as_view(), name='users-signup'),
    url(r'^login/$', LoginView.as_view(), name='users-login'),
    url(r'^logout/$', LogoutView.as_view(), name='users-logout'),
    url(r'^(?P<id>\d+)/$', UserView(), name='users-user'),
)
