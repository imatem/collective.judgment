# -*- coding: utf-8 -*-
from collective.judgment.interfaces import IEvaluation
from plone import api
from plone.app.layout.viewlets import common as base
from Products.CMFCore.permissions import ViewManagementScreens


class Evaluation(base.ViewletBase):

    evaluation = None
    is_manager = None
    userid = None

    def update(self):
        super(Evaluation, self).update()
        if self.evaluation is None:
            self.evaluation = IEvaluation(self.context)
        if self.is_manager is None:
            self.is_manager = api.user.has_permission(
                ViewManagementScreens,
                user=api.user.get_current(),
                obj=self.context)
        if self.userid is None:
            self.userid = api.user.get_current().getId()

    def evaluated(self):
        return self.evaluation.already_evaluated(self.userid)
