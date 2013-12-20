# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from questions.views import QuestionDetail, NewQuestionAjaxView, NewAnswerAjaxView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<id>\d+)/$', QuestionDetail(), name='questions-question_detail'),
    url(r'^new/$', NewQuestionAjaxView(), name='questions-new_question_form'),
    url(r'^(?P<id>\d+)/answer/new/$', NewAnswerAjaxView(), name='questions-new_answer'),
)

