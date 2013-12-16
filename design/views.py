from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth import get_user_model

from questions.models import Question


User = get_user_model()


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        users = User.objects.all()
        return render(request, self.template_name,
                        {'questions': questions,
                         'users': users})
