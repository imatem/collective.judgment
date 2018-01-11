# -*- coding: utf-8 -*-
from collective.judgment import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import alsoProvides
from zope import schema


class IPersonalData(model.Schema):

    title = schema.TextLine(
        title=u"Title",
        description=u"A title, which will be converted to a name",
        required=True
    )

    first_name = schema.TextLine(
        title=_(u'First Name'),
        required=True,
    )

    last_name = schema.TextLine(
        title=_(u'Last Name'),
        required=True,
    )


alsoProvides(IPersonalData, IFormFieldProvider)
