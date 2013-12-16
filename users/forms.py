from django import forms
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

User = auth.get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=30,
        required=True,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput()
    )

    def clean(self):
        if self.errors:
            return self.cleaned_data
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            u = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("user '%s' not exist" % username)
        else:
            if u.check_password(password):
                user = auth.authenticate(**self.cleaned_data)
                if user:
                    self.user = user
                    return self.cleaned_data
                else:
                    raise forms.ValidationError('validate error,try later')
            else:
                raise forms.ValidationError('password not correct')


class SignupForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=30,
        required=True,
        error_messages={'required': 'Username is Required'},
        widget=forms.TextInput(attrs={'autocomplete':'off'})
    )
    password = forms.CharField(
        label=_("Password"),
        required=True,
        error_messages={'required': 'Password is Required'},
        widget=forms.PasswordInput(attrs={'autocomplete':'off'})
    )
    password_confirm = forms.CharField(
        label=_("Password(again)"),
        required=True,
        error_messages={'required': 'Confirm your password'},
        widget=forms.PasswordInput(attrs={'autocomplete':'off'})
    )
    email = forms.EmailField(
        error_messages={'required': 'Email is required',
                        'invalid': 'Email format invalid'}
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
            print 'already exsit'
            raise forms.ValidationError('user "%s" already exists' \
                                            % username)
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data['password_confirm']
        if password!=password_confirm:
            print 'two input password not the same'
            raise forms.ValidationError('two input password not the same')
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



