from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model

from questions.models import Question, Tag


User = get_user_model()


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        tag_name = request.GET.get('tag', '')
        if tag_name:
            tag = get_object_or_404(Tag, name=tag_name)
            questions = tag.questions.all()
            users = set()
            for question in questions:
                users.add(question.asker)
            related = User.objects.filter(answer__question__in=questions)
            for user in related:
                users.add(user)
        else:
            questions = Question.objects.all()[:10]
            tag = None
            users = User.objects.all()[:10]
        tags = Tag.objects.all()[:36]
        return render(request, self.template_name,
                        {'questions': questions,
                         'tags': tags,
                         'tag': tag,
                         'users': users})
