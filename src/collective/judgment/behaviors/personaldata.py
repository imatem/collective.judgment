# -*- coding: utf-8 -*-
from collective.judgment import _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides


class IPersonalData(model.Schema):

    # directives.order_before(title='evaluation_date')
    classification = schema.Choice(
        title=_(u'Classification'),
        vocabulary='collective.judgment.ClassificationsVocabulary',
        required=True
    )
    title = schema.TextLine(
        title=u"Title",
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

    current_position = schema.Choice(
        title=_(u'Current Position'),
        vocabulary='collective.judgment.PositionsVocabulary',
        required=True
    )


alsoProvides(IPersonalData, IFormFieldProvider)
