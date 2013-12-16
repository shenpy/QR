from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import auth
from django.http import response, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext, loader
from django.views.generic.edit import View, FormView

from users.forms import LoginForm, SignupForm


from users.models import User


class UserView:

    def __call__(self, request, **kwargs):
        if request.user.is_authenticated() and \
            request.user.id == int(kwargs['id']):
            return HttpResponseRedirect(reverse_lazy('users-user_home'))
        user = get_object_or_404(User, pk=kwargs['id'])
        questions = user.question_set.order_by('create_date')
        template = loader.get_template("users/user.html")
        context = RequestContext(request, {
            'questions': questions,
            'username': user.username

        })
        print request
        return HttpResponse(template.render(context))


class UserHomeView:

    def __call__(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('users-login'))
        user = request.user
        questions = user.question_set.order_by('create_date')
        template = loader.get_template("users/user_home.html")
        context = RequestContext(request, {
            'questions': questions,
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
