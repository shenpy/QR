# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=40)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return u"%s" % self.name

    def build_url(self):
        return u"{0}?tag={1}".format(reverse('index'), self.name)


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    asker = models.ForeignKey(User)
    create_date = models.DateTimeField(default=datetime.now)
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)

    def __unicode__(self):
        return u"%s" % self.title


class Answer(models.Model):
    replyer = models.ForeignKey(User)
    text = models.TextField()
    question = models.ForeignKey(Question, related_name='answers')
    score = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, related_name='voted', \
                                            through='Vote')
    create_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return u"%s" % self.text


class Vote(models.Model):
    answer = models.ForeignKey(Answer)
    voter = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s, by %s' % (self.answer, self.voter)

    class Meta:
        unique_together = (('answer', 'voter'),)


@receiver(post_save, sender=Vote)
def on_create_vote(sender, instance, signal, created, **kwargs):
    if created:
        answer = instance.answer
        answer.score += 1
        answer.save()

@receiver(post_delete, sender=Vote)
def on_delete_vote(sender, instance, signal, **kwargs):
    answer = instance.answer
    answer.score -= 1
    answer.save()

