# -*- coding: utf-8 -*-
from collective.judgment.interfaces import IEvaluation
from plone import api
from plone.app.layout.viewlets import common as base
from Products.CMFCore.permissions import ViewManagementScreens


class Evaluation(base.ViewletBase):

    vote = None
    is_manager = None

    def update(self):
        super(Evaluation, self).update()

        if self.vote is None:
            self.vote = IEvaluation(self.context)
        if self.is_manager is None:
            self.is_manager = api.user.has_permission(
                ViewManagementScreens,
                user=api.user.get_current(),
                obj=self.context)

    def voted(self):
        return self.vote.already_voted(self.request)

    def average(self):
        return self.vote.average_vote()

    def has_evaluations(self):
        return self.vote.has_evaluations()
