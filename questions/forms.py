# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from questions.models import Question


class QuestionForm(ModelForm):
    #title = forms.CharField(max_length=255,
     #                       label=mark_safe('Title<br/>'))
    title = forms.CharField(max_length=255,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'title',
                                      'class': 'question-input'})
    )
    description = forms.CharField(
         label='',
         widget=forms.Textarea(attrs={'placeholder': 'description',
                                        'class': 'question-input'}),
    )

    class Meta:
        model = Question
        exclude = ['create_date', 'asker']


class AnswerForm(forms.Form):
    text = forms.Textarea()
