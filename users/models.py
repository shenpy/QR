# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


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
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ PermissionsMixin auto add field to your model: is_superuser"""
    username = models.CharField(max_length=40, unique=True,
                                        db_index=True)
    email = models.EmailField(max_length=254, unique=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', db_table='user_relationship', blank=True)

    #is_active = models.BooleanField(default=True)
    #is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return unicode(self.username)

    def get_short_name(self):
        return u"%s" % self.username

    def get_username(self):
        return u"%s" % self.username
