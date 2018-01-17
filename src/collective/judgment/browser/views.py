# -*- coding: utf-8 -*-
from collective.judgment.interfaces import IEvaluation
from plone.dexterity.browser.view import DefaultView
from Products.Five import BrowserView
from plone import api


class PromotionView(DefaultView):
    """ The default view for talks
    """

    def foo(self):
        return ''


class FolderCdimView(BrowserView):


    def __init__(self, context, request):
        self.context = context
        self.request = request

    def itembrains(self):

        option = 'pending'
        if self.request.form:
            option = self.request.form.get('options', 'pending')

        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(
            path=dict(query='/'.join(self.context.getPhysicalPath()), depth=1),
            review_state=option,
            # sort_on='start'
        )

        return brains

    def evaluations(self, brain):

        values = IEvaluation(brain.getObject()).evaluations

        evaluators = []

        isManager = self.isManager()
        userid = api.user.get_current().id

        for gmember in api.user.get_users(groupname='evaluators'):
            if isManager:
                evaluators.append((gmember.getProperty('fullname'), values.get(gmember.id, None), gmember.id))
            elif userid == gmember.id:
                evaluators.append((gmember.getProperty('fullname'), values.get(gmember.id, None), gmember.id))
                break
        return evaluators

    def isManager(self):

        local_roles = self.context.portal_membership.getAuthenticatedMember().getRolesInContext(self.context)
        if 'Manager' in local_roles or 'Reviewer' in local_roles:
            return True
        return False
