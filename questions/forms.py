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
        widget=forms.TextInput(attrs={'placeholder': '标题',
                                      'class': 'question-input'})
    )
    description = forms.CharField(
         label='',
         widget=forms.Textarea(attrs={'placeholder': \
                                u"""描述你遇到的问题:
                                    >可以使用"#标记#"的方式对问题分类
                                    >可以使用"@用户名"的方式寻求帮助""",
                                    'class': 'question-input'}),
    )

    class Meta:
        model = Question
        exclude = ['create_date', 'asker', 'tags']


class AnswerForm(forms.Form):
    text = forms.CharField(
         label='',
         error_messages={'required': 'please input your Comment'},
         widget=forms.Textarea(attrs={'placeholder': 'your answer',
                                      'rows': 3,
                                      'class': 'question-input'}),
    )
