# -*- coding: utf-8 -*-
from collective.judgment.interfaces import IEvaluable
from collective.judgment.interfaces import IEvaluation
from persistent.list import PersistentList
from plone import api
from zope.publisher.browser import BrowserPage
from z3c.form import button
from z3c.form import form

import logging

logger = logging.getLogger(__name__)


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


class UpdateEvaluations(form.Form):
    """docstring for UpdateEvaluations"""

    @button.buttonAndHandler(u'Update pending evaluations')
    def handle_update_evaluations(self, action):
        """ update list of evaluators in objects pending for review.
        """
        # code from upgrades.py
        brains = api.content.find(
            object_provides=IEvaluable, review_state='pending')
        for evaluable in brains:
            evaluations = IEvaluation(evaluable.getObject()).evaluations
            evaluations.pop('mochan')
            for user in api.user.get_users(groupname='evaluators'):
                if user.id not in evaluations:
                    evaluations[user.id] = PersistentList()
                    logger.info('Adding {} to {}'.format(
                        user.id, evaluable.Title.encode('utf-8')))
            logger.info('{} has {} evaluators'.format(
                evaluable.Title.encode('utf-8'), len(evaluations)))
