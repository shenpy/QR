# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import auth
from django.http import response, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext, loader
from django.views.generic.edit import View, FormView

from users.forms import LoginForm, SignupForm
from users.models import User
from notifications.models import Activity, Notification
from questions.models import Answer


class ExtraMixin:

    def get_extra_context(self):
        context = {}
        user = self.request.user
        if user.is_authenticated():
            notifications_count = Notification.objects.filter(receiver=user, is_read=False).count()
            context['notifications_count'] = notifications_count
        return context



class UserView(ExtraMixin):

    def __call__(self, request, **kwargs):
        self.request = request
        if request.user.is_authenticated() and \
            request.user.id == int(kwargs['id']):
            return HttpResponseRedirect(reverse_lazy('users-user_home'))
        user = get_object_or_404(User, pk=kwargs['id'])
        asked_questions = user.question_set.order_by('create_date')
        answers = Answer.objects.select_related('question').filter(replyer=user)
        replyed_questions = set(answer.question for answer in answers)
        template = loader.get_template("users/user.html")
        context = RequestContext(request, {
            'asked_questions': asked_questions,
            'replyed_questions': replyed_questions,
            'other': user

        })
        context.update(self.get_extra_context())
        return HttpResponse(template.render(context))


class UserHomeView:

    def __call__(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('users-login'))
        user = request.user
        asked_questions = user.question_set.order_by('create_date')
        template = loader.get_template("users/user_home.html")
        answers = Answer.objects.select_related('question').filter(replyer=user)
        replyed_questions = set(answer.question for answer in answers)
        context = RequestContext(request, {
            'asked_questions': asked_questions,
            'replyed_questions': replyed_questions,
            'is_me': True
        })
        return HttpResponse(template.render(context))


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('users-user_home')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        #remove : in field label
        form.label_suffix = ' '
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        auth.login(self.request, form.user)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse_lazy('users-login'))


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('users-user_home')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        #remove : in field label
        form.label_suffix = ' '
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        User.objects.create_user(**form.cleaned_data)
        user = auth.authenticate(**form.cleaned_data)
        auth.login(self.request, user)
        return super(SignupView, self).form_valid(form)


def follow(request, id):
    user = request.user
    if user.is_authenticated():
        following = get_object_or_404(User, pk=id)
        user.following.add(id)
        user.save()
        user_href = reverse('users-user', args=(user.id,))
        following_href = reverse('users-user', args=(following.id,))
        user_tag = \
                   u'<a href="{0}">{1}</a>'.format(user_href, user.username)
        following_tag = \
                   u'<a href="{0}">{1}</a>'.format(following_href, following.username)
        text = u'{0}关注了{1}'.format(user_tag, following_tag)
        activity = Activity(text=text, user=user)
        activity.save()
        receivers = [following]
        activity.notify(receivers)
        return HttpResponse()
    else:
        return HttpResponseRedirect(reverse_lazy('users-login'))


def unfollow(request, id):
    user = request.user
    if user.is_authenticated():
        user.following.remove(id)
        user.save()
        return HttpResponse()
    else:
        return HttpResponseRedirect(reverse_lazy('users-login'))


