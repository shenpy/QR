# -*- coding: utf-8 -*-
from django.test import TestCase

from django.contrib.auth import get_user_model
from questions.models import *

User = get_user_model()


class QuestionsTestCase(TestCase):
    """test Question model methods"""
    fixtures = ['questions_models.json']

    def test_on_vote_create(self):
        voter_john = User(username='john', email='john@qq.com')
        voter_john.save()
        asker_doe = User(username='doe', email='doe@qq.com')
        asker_doe.save()
        john_one = User(username='john doe', email='john2@qq.com')
        john_one.save()
        question = Question(title='how to',
                            description="i don't know how to...")
        question.asker = asker_doe
        question.save()
        answer1 = Answer(text='well, i know', question=question)
        answer1.replyer = john_one
        answer1.save()
        self.assertEqual(answer1.score, 0)
        vote = Vote(voter=voter_john, answer=answer1)
        vote.save()
        self.assertEqual(answer1.score, 1)

    def test_on_vote_delete(self):
        voter_john = User(username='john', email='john@qq.com')
        voter_john.save()
        asker_doe = User(username='doe', email='doe@qq.com')
        asker_doe.save()
        john_one = User(username='john doe', email='john2@qq.com')
        john_one.save()
        question = Question(title='how to',
                            description="i don't know how to...")
        question.asker = asker_doe
        question.save()
        answer1 = Answer(text='i know, you should ...', question=question)
        answer1.replyer = john_one
        answer1.save()
        self.assertEqual(answer1.score, 0)
        vote = Vote(voter=voter_john, answer=answer1)
        vote.save()
        self.assertEqual(answer1.score, 1)
        vote.delete()
        self.assertEqual(answer1.score, 0)
