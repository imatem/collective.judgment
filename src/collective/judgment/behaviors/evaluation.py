# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations


KEY = "collective.judgment.behaviors.evaluation.Evaluation"


class Evaluation(object):
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if KEY not in annotations.keys():
            annotations[KEY] = PersistentDict({'evaluations': PersistentDict()})
        self.annotations = annotations[KEY]

    @property
    def evaluations(self):
        return self.annotations['evaluations']

    def evaluate(self, evaluation, userid):
        if self.already_evaluated(userid):
            raise KeyError("You may not evaluate twice")
        evaluations = self.annotations['evaluations']
        evaluations[userid] = evaluation

    def already_evaluated(self, userid):
        return userid in self.annotations['evaluations'].keys()

    def clear(self):
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict({'evaluations': PersistentDict()})
        self.annotations = annotations[KEY]
