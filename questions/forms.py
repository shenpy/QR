# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from questions.models import Question


class QuestionForm(ModelForm):
    title = forms.CharField(max_length=255,
                            label=mark_safe('Title<br/>'))
    description = forms.TextInput()

    class Meta:
        model = Question
        exclude = ['create_date', 'asker']


class AnswerForm(forms.Form):
    text = forms.TextInput()

