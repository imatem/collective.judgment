# -*- coding: utf-8 -*-
from collective.judgment.interfaces import IEvaluation
from zope.publisher.browser import BrowserPage


class Vote(BrowserPage):

    def __call__(self, rating):
        voting = IEvaluation(self.context)
        voting.vote(rating, self.request)
        return 'success'


class ClearVotes(BrowserPage):

    def __call__(self, rating):
        voting = IEvaluation(self.context)
        voting.clear()
        return 'success'
