# -*- coding: utf-8 -*-
from django import forms
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

User = auth.get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={'required': u'请输入用户名'},
        label='',
        widget=forms.TextInput(attrs={'placeholder': u'用户名'}),
        max_length=30,
        required=True,
    )
    password = forms.CharField(
        error_messages={'required': u'请输入密码'},
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': '密码'}),
        required=True,
    )

    def clean(self):
        if self.errors:
            return self.cleaned_data
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            u = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError(u'用户"%s"不存在' % username)
        else:
            if u.check_password(password):
                user = auth.authenticate(**self.cleaned_data)
                if user:
                    self.user = user
                    return self.cleaned_data
                else:
                    raise forms.ValidationError(u'服务器异常，稍后再试')
            else:
                raise forms.ValidationError(u'密码错误')


class SignupForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=30,
        required=True,
        error_messages={'required': u'用户名必须填写'},
        widget=forms.TextInput(attrs={'autocomplete':'off',
                                      'placeholder': u'用户名'})
    )
    password = forms.CharField(
        label='',
        required=True,
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(attrs={'autocomplete':'off',
                                          'placeholder': u'密码'})
    )
    password_confirm = forms.CharField(
        label='',
        required=True,
        error_messages={'required': u'请再次输入密码'},
        widget=forms.PasswordInput(attrs={'autocomplete':'off',
                                          'placeholder': u'确认密码'})
    )
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': u'邮箱'}),
        error_messages={'required': u'请输入邮箱',
                        'invalid': u'邮箱格式错误'}
    )

    def clean_username(self):
        # if a required field is unfilled,
        # clean_field method won't be called
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            pass
        else:
            raise forms.ValidationError(u'用户名"%s"已经存在' \
                                            % username)
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data['password_confirm']
        if password!=password_confirm:
            raise forms.ValidationError(u'两次密码输入不一致')
        return password_confirm

    def clean(self):
        # clean_fieldname is called before clean
        #'but' if error happens , it will log it in self.errors
        # and keep doing clean() thus made users know all errors in a time
        # prevent user from posting error post  many times

        # use .get() method won't raise exception
        # clean() should be used in special customized condition

        if self.errors:
        #but use this use won't log the errors after it
        #thus he may post again with  after errors

            return self.cleaned_data
        else:
            ## doing some other futher clean or operation
            ## when all fields no error but
            ## still have othrt thing to validate
            del self.cleaned_data['password_confirm']
            return self.cleaned_data



