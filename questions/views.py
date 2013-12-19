# -*- coding: utf-8 -*-
from functools import wraps

from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from questions.models import *
from questions.forms import QuestionForm


from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, \
                        HttpResponseNotAllowed

from django.template import RequestContext, loader, Context

User = get_user_model()


class QuestionDetail:

    def __call__(self, request, id):
        question = get_object_or_404(Question, id=id)
        json = serializers.serialize("json", [question])
        return HttpResponse(json, mimetype="application/json")

class NewQuestionAjaxView:

    def require_AJAX(function):
        """Return a bad request instance if the view is not using AJAX
        function -- the view
        """

        wraps(function)
        def wrap(self, request):
            permission = (
                    request.is_ajax(),
                    request.user.is_authenticated()
            )
            if not all(permission):
                return HttpResponseNotAllowed('AJAX')
            self.request=request
            print request
            return function(self, request)

        #wrap.__doc__ = function.__doc__
        #wrap.__name__ = function.__name__
        return wrap

    def __call__(self, request):
        self.request=request
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            allowed_methods = [m.lstrip("do_") for m in dir(self)
                                                if m.startswith("do_")]
            return HttpResponseNotAllowed(allowed_methods)
        return callback()

    def do_GET(self):
        if self.request.user.is_authenticated():
            form = QuestionForm()
            form.label_suffix=''
            context = RequestContext(self.request, {'form': form})
            template  = loader.get_template('questions/ajax_new_question_form.html')
            return HttpResponse(template.render(context))
        else:
            return HttpResponseRedirect('/')

    def do_POST(self):
        form = QuestionForm(self.request.POST)
        if form.is_valid():
            print form
            question = Question(title=form.cleaned_data['title'],
                                description=form.cleaned_data['description'],
                                asker = self.request.user)
            question.save()
            return HttpResponseRedirect(reverse('questions-question_detail', args=(question.id,)))
