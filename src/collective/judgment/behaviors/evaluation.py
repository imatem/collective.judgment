# -*- coding: utf-8 -*-
from DateTime import DateTime
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from plone import api
from zope.annotation.interfaces import IAnnotations


KEY = 'collective.judgment.behaviors.evaluation.Evaluation'


class Evaluation(object):
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        # if KEY not in annotations.keys():
        #     annotations[KEY] = PersistentDict({'evaluations': PersistentDict()})
        self.annotations = annotations[KEY]

    @property
    def evaluations(self):
        return self.annotations

    def evaluate(self, evaluation, userid):
        # if not self.already_evaluated(userid):
        #     self.evaluations[userid] = PersistentList()

        evaluations = self.annotations[userid]
        evaluations.insert(0, PersistentDict(
            {'evaluation': evaluation, 'date': DateTime()})
        )

    def already_evaluated(self, userid):
        return userid in self.annotations and self.annotations[userid] != []

    def clear(self):
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict()
        self.annotations = annotations[KEY]
        for member in api.user.get_users(groupname='evaluators'):
            self.annotations[member.id] = PersistentList()
