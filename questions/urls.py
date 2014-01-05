# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from questions.views import QuestionDetail, \
                            NewQuestionAjaxView, NewAnswerAjaxView, \
                            vote, unvote


urlpatterns = patterns('',
    url(r'^(?P<id>\d+)/$', QuestionDetail(), name='questions-question_detail'),
    url(r'^new/$', NewQuestionAjaxView(), name='questions-new_question_form'),
    url(r'^(?P<id>\d+)/answer/new/$', NewAnswerAjaxView(), name='questions-new_answer'),
    url(r'^answer/(?P<id>\d+)/vote/$', vote, name='questions-answer_vote'),
    url(r'^answer/(?P<id>\d+)/unvote/$', unvote, name='questions-answer_unvote'),
)
