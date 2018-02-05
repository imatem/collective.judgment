# -*- coding: utf-8 -*-
from collective.judgment import _
from plone.app.contenttypes.content import File
# from plone.dexterity.content import Container
from zope import schema
from plone.supermodel import model
from plone.namedfile import field as namedfile

from collective.judgment.validators import isValidFileType
from plone.autoform import directives


class IPdfFile(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Promotion
    """
    title = schema.TextLine(
        title=_(u'Title'),
        # description=u"",
        required=False
    )

    description = schema.Text(
        title=_(u'Description'),
        # description=u"",
        required=False
    )

    file = namedfile.NamedBlobFile(
        title=_(u'File'),
        required=True,
        constraint=isValidFileType,
        # primary=True,
    )
    model.primary('file')

    directives.omitted('thumbfile')
    thumbfile = namedfile.NamedBlobImage(
        title=_(u'ImageThumb'),
        required=False,
    )


class CurriculumVitae(File):
    """Convenience subclass for ``Curriculum Vitae`` portal type
    """


class ActivitiesPlan(File):
    """Convenience subclass for ``Activities Plan`` portal type
    """


class ActivitiesReport(File):
    """Convenience subclass for ``Activities Report`` portal type
    """
