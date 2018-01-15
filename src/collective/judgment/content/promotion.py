# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
from collective.judgment import _
from collective.judgment.validators import isValidFileType
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from zope.interface import implementer


class IPromotion(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Promotion
    """

    cv = namedfile.NamedBlobFile(
        title=_(u'Curriculum vitae (Gold-sponsors and above)'),
        required=True,
        constraint=isValidFileType,
    )

    directives.omitted('thumbcv')
    thumbcv = namedfile.NamedBlobImage(
        title=_(u'ImageThumb'),
        required=False,
    )

    report = namedfile.NamedBlobFile(
        title=_(u'Activities Report'),
        required=True,
        constraint=isValidFileType,
    )

    directives.omitted('thumbreport')
    thumbreport = namedfile.NamedBlobImage(
        title=_(u'ImageThumbReport'),
        required=False,
    )

    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IPromotion)
class Promotion(Container):
    """
    """
