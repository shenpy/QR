# -*- coding: utf-8 -*-
from functools import wraps

from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import simplejson

from questions.models import *
from questions.forms import QuestionForm, AnswerForm

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotAllowed, HttpResponseForbidden

from django.template import RequestContext, loader, Context

User = get_user_model()


class MyBaseView:

    def require_AJAX(function):
        """Return a bad request instance if the view is not using AJAX
        function -- the view
        """

        wraps(function)
        def wrap(self, request, *args, **kwargs):
            permission = (
                    request.is_ajax(),
                    request.user.is_authenticated()
            )
            if not all(permission):
                return HttpResponseNotAllowed('AJAX')
            self.request=request
            return function(self, request, *args, **kwargs)
        #wrap.__doc__ = function.__doc__
        #wrap.__name__ = function.__name__
        return wrap

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.request=request
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            allowed_methods = [m.lstrip("do_") for m in dir(self)
                                                if m.startswith("do_")]
            return HttpResponseNotAllowed(allowed_methods)
        return callback(*args, **kwargs)


class QuestionDetail:

    def __call__(self, request, id):
        question = get_object_or_404(Question, id=id)
        #json = serializers.serialize("json", [question])
        #return HttpResponse(json, mimetype="application/json")
        answerform = AnswerForm()
        user = request.user
        if user.is_authenticated():
            answers = question.answers.select_related('voter').extra(select={'is_voted': 'id In (%s)' % user.voted.values('id').query})
        else:
            answers = question.answers.select_related('voter')
        context = RequestContext(request, {'question': question,
                                           'answers': answers,
                                           'answerform': answerform})
        template  = loader.get_template('questions/question_detail.html')
        return HttpResponse(template.render(context))


class NewQuestionAjaxView(MyBaseView):

    def do_GET(self, *args, **kwargs):
        form = QuestionForm()
        form.label_suffix=''
        context = RequestContext(self.request, {'form': form})
        template  = loader.get_template('questions/ajax_new_question_form.html')
        return HttpResponse(template.render(context))

    def do_POST(self, *args, **kwargs):
        form = QuestionForm(self.request.POST)
        if form.is_valid():
            question = Question(title=form.cleaned_data['title'],
                                description=form.cleaned_data['description'],
                                asker = self.request.user)
            question.save()
            return HttpResponseRedirect(reverse('questions-question_detail', args=(question.id,)))
        return HttpResponseRedirect('/')


class NewAnswerAjaxView(MyBaseView):

    def do_POST(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            answerform = AnswerForm(self.request.POST)
    # is     there better way to save answer with its question so i don'r need to get question
    # yep  set foreignkey using integer  '''field_id = kwargs['id']'''
            if answerform.is_valid():
                answer = Answer(text=answerform.cleaned_data['text'])
                answer.replyer = self.request.user
                answer.question_id = kwargs['id']
                answer.save()
                json = serializers.serialize("json", [answer])
                return HttpResponse(json, mimetype="application/json")
            else:
                errors = answerform.errors
                response =  HttpResponse(simplejson.dumps(errors))
                response.status_code = 400
                return response
        else:
            return HttpResponseForbidden()


def vote(request, id):
    user = request.user
    if user.is_authenticated():
        vote, created= Vote.objects.get_or_create(answer_id=id, voter=user)
        vote.save()
        return HttpResponse()
    else:
        return HttpResponseForbidden()


def unvote(request, id):
    user = request.user
    if user.is_authenticated():
        vote = get_object_or_404(Vote, answer_id=id, voter=user)
        vote.delete()
        return HttpResponse()
    else:
        return HttpResponseForbidden()
