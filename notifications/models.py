from django.db import models
from django.utils import timezone

from users.models import User

class Activity(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_activities'

    def notify(self, receivers):
        for receiver in receivers:
            Notification.objects.get_or_create(text=self.text,
                                               receiver=receiver)


class Notification(models.Model):
    text = models.TextField()
    receiver = models.ForeignKey(User)
    is_read = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)

