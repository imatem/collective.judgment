# -*- coding: utf-8 -*-
from collective.judgment import _
from collective.judgment.validators import isValidFileType
from plone.app.contenttypes.content import File
from plone.autoform import directives
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def request_title(context):
    return context.REQUEST.form.get('title', '')


class IPdfFile(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Promotion
    """
    # directives.omitted('title')
    title = schema.TextLine(
        title=_(u'Title'),
        # description=u"",
        required=False,
        defaultFactory=request_title,
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


class PdfFile(File):
    """Convenience subclass for ``File`` only accept pdf
    """
