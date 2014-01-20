# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have username')
        user = self.model(
            username=username,
            email=MyUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True,
                                        db_index=True)
    email = models.EmailField(max_length=254, unique=True)
    relating = models.ManyToManyField('self',
                                      symmetrical=False,
                                      through='Relationship',
                                      related_name='related_to')

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return unicode(self.username)

    @property
    def last_active(self):
        return cache.get('active_%s' % self.username)

    @property
    def is_online(self):
        if self.last_active:
            now = datetime.datetime.now()
            if now > self.last_active + datetime.timedelta(
                        seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    @property
    def followings(self):
        return self.get_relating(RELATIONSHIP_FOLLOWING)

    @property
    def followers(self):
        return self.get_related(RELATIONSHIP_FOLLOWING)

    def add_following(self, user):
        self.add_relationship(user, RELATIONSHIP_FOLLOWING)

    def remove_following(self, user):
        self.remove_relationship(user, RELATIONSHIP_FOLLOWING)

    def add_relationship(self, user, status):
        relationship, created = Relationship.objects.get_or_create(
            from_user=self,
            to_user=user,
            status=status)
        return relationship

    def remove_relationship(self, user, status):
        Relationship.objects.filter(
            from_user=self,
            to_user=user,
            status=status).delete()
        return

    def get_relating(self, status):
        return self.relating.filter(
            to_user__status=status,
            to_user__from_user=self)

    def get_related(self, status):
        return self.related_to.filter(
            from_user__status=status,
            from_user__to_user=self)


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)


