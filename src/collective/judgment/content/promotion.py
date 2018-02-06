# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
from collective.judgment import _
# from collective.judgment.validators import isValidFileType
# from plone.autoform import directives
from plone.dexterity.content import Container
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


class IPromotion(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Promotion
    """

    # directives.widget(level=RadioFieldWidget)
    requestedposition = schema.Choice(
        title=_(u'Requested position'),
        vocabulary='collective.judgment.PositionsVocabulary',
        required=True
    )


@implementer(IPromotion)
class Promotion(Container):
    """
    """
