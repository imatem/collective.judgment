# -*- coding: utf-8 -*-
# from collective.judgment import _
from Acquisition import aq_inner
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import addContentToContainer
from zope.component import getUtility


class PdfFileAddForm(DefaultAddForm):
    portal_type = 'Pdf File'

    def add(self, object):

        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        new_object = addContentToContainer(container, object)

        parentfti = getUtility(IDexterityFTI, name=container.portal_type)

        if parentfti.immediate_view:
            self.immediate_view = "/".join(
                [container.absolute_url(), fti.immediate_view]
            )
        else:
            self.immediate_view = "/".join(
                [container.absolute_url(), ]
            )


class PdfFileAddView(DefaultAddView):
    form = PdfFileAddForm
