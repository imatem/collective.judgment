# -*- coding: utf-8 -*-
from collective.judgment import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import alsoProvides
from zope import schema


class IBasicInfo(model.Schema):

    first_name = schema.TextLine(
        title=_(u'First Name'),
        required=True,
    )

    last_name = schema.TextLine(
        title=_(u'Last Name'),
        required=True,
    )

alsoProvides(IBasicInfo, IFormFieldProvider)
