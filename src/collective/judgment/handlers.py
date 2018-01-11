# -*- coding: utf-8 -*-
from collective.judgment.content.promotion import IPromotion
from plone import namedfile
from zope.component import adapter
# from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


import os
import tempfile
import shutil


@adapter(IPromotion, IObjectAddedEvent)
def handlerAddedPromotion(self, event):

    try:

        tempdir = tempfile.mkdtemp()
        file_path = os.path.join(tempdir, 'cv.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.cv.data)
        file_os.close()
        os.system("cd {0}; gs -o page1.png -sDEVICE=pngalpha -dLastPage=1 {1}".format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'page1.png')
        thumb_file = open(image_path, 'r')

        self.thumbcv = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'page1.png'
        )
    except:
        self.thumbcv = None

    try:
        shutil.rmtree(tempdir)  # remove tempdir
    except:
        pass



@adapter(IPromotion, IObjectModifiedEvent)
def handlerModifiedPlan(self, event):

    try:

        tempdir = tempfile.mkdtemp()
        file_path = os.path.join(tempdir, 'cv.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.cv.data)
        file_os.close()
        os.system("cd {0}; gs -o page1.png -sDEVICE=pngalpha -dLastPage=1 {1}".format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'page1.png')
        thumb_file = open(image_path, 'r')

        self.thumbcv = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'page1.png'
        )
    except:
        self.thumbcv = None

    try:
        shutil.rmtree(tempdir)  # remove tempdir
    except:
        pass
