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
        evaluators = [i.id for i in api.user.get_users(groupname='evaluators')]
        for evaluable in brains:
            obj = evaluable.getObject()
            evaluations = IEvaluation(obj).evaluations
            inactive = [i for i in evaluations if i not in evaluators]
            for userid in inactive:
                api.user.revoke_roles(username=userid, roles=['Reader'], obj=obj)
                evaluations.pop(userid)
                logger.info('remove {} from evaluators'.format(userid))

            for userid in evaluators:
                if userid not in evaluations:
                    evaluations[userid] = PersistentList()
                    api.user.grant_roles(username=userid, roles=['Reader'], obj=obj)
                    logger.info('Adding {} to {}'.format(
                        userid, evaluable.Title.encode('utf-8')))
            logger.info('{} has {} evaluators'.format(
                evaluable.Title.encode('utf-8'), len(evaluations)))


class UpdateStudiedEvaluations(form.Form):

    @button.buttonAndHandler(u'Update evaluations, change local roles')
    def handle_update_evaluations(self, action):
        """This method is meant to be used only once
        """
        # code from upgrades.py
        brains = api.content.find(object_provides=IEvaluable)

        for brain in brains:
            obj = brain.getObject()
            evaluations = IEvaluation(obj).evaluations
            for xid in evaluations.keys():
                api.user.grant_roles(username=xid, roles=['Reader'], obj=obj)
            api.content.disable_roles_acquisition(obj=obj)
            api.group.grant_roles(groupname='Reviewers', roles=['Reader'], obj=obj)
        logger.info('listo')
