# -*- coding: utf-8 -*-
from collective.judgment.interfaces import IEvaluation
from plone import api
from zope.publisher.browser import BrowserPage


class Evaluate(BrowserPage):

    def __call__(self, rating):
        evaluation = IEvaluation(self.context)
        current = api.user.get_current()
        evaluation.evaluate(rating, current.getId())
        return 'success'


class ClearEvaluations(BrowserPage):

    def __call__(self, rating):
        evaluation = IEvaluation(self.context)
        evaluation.clear()
        return 'success'
