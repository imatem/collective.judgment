# -*- coding: utf-8 -*-
from collective.judgment import _
from collective.judgment.behaviors.evaluation import KEY
from collective.judgment.content.promotion import IPromotion
from collective.judgment.content.files import IPdfFile
from persistent.dict import PersistentDict
from plone import namedfile
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zope.lifecycleevent import ObjectModifiedEvent
from zope.container.contained import ContainerModifiedEvent
from zope.interface import Invalid
from Products.statusmessages.interfaces import IStatusMessage

import os
import shutil
import tempfile


@adapter(IPromotion, IObjectCreatedEvent)
def handlerCreatedPromotion(self, event):
    annotations = IAnnotations(self)
    if KEY not in annotations:
        annotations[KEY] = PersistentDict({'evaluations': PersistentDict()})


# @adapter(IPromotion, IObjectAddedEvent)
# def handlerAddedPromotion(self, event):

@adapter(IPromotion, IObjectModifiedEvent)
def handlerModifiedPromotion(self, event):

    if type(event) == ContainerModifiedEvent:
        cv = [item[1] for item in self.items() if item[1].portal_type == 'Curriculum Vitae']
        if len(cv) > 1:
            IStatusMessage(self.REQUEST).addStatusMessage(_(u'There were errors.'), 'error')



@adapter(IPdfFile, IObjectAddedEvent)
def handlerAddedPdfFile(self, event):
    tempdir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(tempdir, 'file.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.file.data)
        file_os.close()
        os.system('cd {0}; gs -o page1.png -sDEVICE=pngalpha -dLastPage=1 {1}'.format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'page1.png')
        thumb_file = open(image_path, 'r')

        self.thumbfile = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'page1.png'
        )
    except:
        self.thumbfile = None

    try:
        shutil.rmtree(tempdir)  # remove tempdir
    except:
        pass


@adapter(IPdfFile, IObjectModifiedEvent)
def handlerModifiedPdfFile(self, event):
    tempdir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(tempdir, 'file.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.file.data)
        file_os.close()
        os.system('cd {0}; gs -o page1.png -sDEVICE=pngalpha -dLastPage=1 {1}'.format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'page1.png')
        thumb_file = open(image_path, 'r')

        self.thumbfile = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'page1.png'
        )
    except:
        self.thumbfile = None

    try:
        shutil.rmtree(tempdir)  # remove tempdir
    except:
        pass
