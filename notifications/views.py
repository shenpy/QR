from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.shortcuts import render

from questions.models import Question
from notifications.models import Notification

User = get_user_model()


class NotificationView(View):
    template_name = 'notifications.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('users-login'))
        notifications = Notification.objects.filter(receiver=user, is_read=False)
        for notification in notifications:
            notification.is_read = True
            notification.save()
        return render(request, self.template_name,
                        {'notifications': notifications,
                         'user': user})
