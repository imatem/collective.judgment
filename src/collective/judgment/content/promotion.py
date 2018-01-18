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

    letter = namedfile.NamedBlobFile(
        title=_(u'Letter'),
        required=True,
        constraint=isValidFileType,
    )

    directives.omitted('thumbletter')
    thumbletter = namedfile.NamedBlobImage(
        title=_(u'ImageThumbLetter'),
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

    plan = namedfile.NamedBlobFile(
        title=_(u'Plan'),
        required=True,
        constraint=isValidFileType,
    )

    directives.omitted('thumbplan')
    thumbplan = namedfile.NamedBlobImage(
        title=_(u'ImagePlan'),
        required=False,
    )

    cv = namedfile.NamedBlobFile(
        title=_(u'Curriculum vitae'),
        required=True,
        constraint=isValidFileType,
    )

    directives.omitted('thumbcv')
    thumbcv = namedfile.NamedBlobImage(
        title=_(u'ImageThumb'),
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
