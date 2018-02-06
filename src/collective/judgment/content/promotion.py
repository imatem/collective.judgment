# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
from collective.judgment import _
# from collective.judgment.validators import isValidFileType
from plone.autoform import directives
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
    directives.order_after(requestedposition='IPersonalData.current_position')
    requestedposition = schema.Choice(
        title=_(u'Requested position'),
        vocabulary='collective.judgment.PositionsVocabulary',
        required=True
    )
    directives.order_after(evaluation_date='requestedposition')
    evaluation_date = schema.Date(
        title=_(u'Evaluation Date'),
        required=True,
    )


@implementer(IPromotion)
class Promotion(Container):
    """
    """
