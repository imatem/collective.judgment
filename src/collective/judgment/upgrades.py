# -*- coding: utf-8 -*-
from collective.judgment.interfaces import IEvaluable
from collective.judgment.interfaces import IEvaluation
from persistent.list import PersistentList
from plone import api

import logging

logger = logging.getLogger(__name__)


def upgrade_evaluators(setup):
    # objects already studied
    brains = api.content.find(
        object_provides=IEvaluable, review_state='studied')
    for evaluable in brains:
        evaluations = IEvaluation(evaluable.getObject()).evaluations
        for user in api.user.get_users():
            if user.id not in evaluations and user.id != 'erendira':
                evaluations[user.id] = PersistentList()
                logger.info('Adding {} to {}'.format(
                    user.id, brains[0].Title.encode('utf-8')))
        logger.info('{} has {} evaluators'.format(
            brains[0].Title.encode('utf-8'), len(evaluations)))

    # objects to be studied
    brains = api.content.find(
        object_provides=IEvaluable, review_state='pending')
    for evaluable in brains:
        evaluations = IEvaluation(evaluable.getObject()).evaluations
        for user in api.user.get_users(groupname='evaluators'):
            if user.id not in evaluations:
                evaluations[user.id] = PersistentList()
                logger.info('Adding {} to {}'.format(
                    user.id, brains[0].Title.encode('utf-8')))
        logger.info('{} has {} evaluators'.format(
            brains[0].Title.encode('utf-8'), len(evaluations)))
