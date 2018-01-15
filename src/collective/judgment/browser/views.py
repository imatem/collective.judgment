# -*- coding: utf-8 -*-

from plone.dexterity.browser.view import DefaultView
from Products.Five import BrowserView
from plone import api

class PromotionView(DefaultView):
    """ The default view for talks
    """

    def foo(self):
        import pdb; pdb.set_trace()
        return ''


class FolderCdimView(BrowserView):

    def itembrains(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(
            path=dict(query='/'.join(self.context.getPhysicalPath()), depth=1),
            # sort_on='start'
        )

        return brains

    def evaluations(self, brain):

        values = {
            'revisor1': 'approve',
            'revisor2': 'approve',
            # 'revisor3': None,
            'revisor2': 'disapprove',
        }
        evaluators = []
        for gmember in api.user.get_users(groupname='evaluators'):
            # evaluators[gmember.id] = gmember.getProperty('fullname')
            evaluators.append((gmember.getProperty('fullname'), values.get(gmember.id, None)))

        return evaluators
