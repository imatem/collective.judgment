# -*- coding: utf-8 -*-
from collective.judgment.content.promotion import IPromotion
from collective.judgment.behaviors.evaluation import KEY
from persistent.dict import PersistentDict
from plone import namedfile
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

import os
import tempfile
import shutil


@adapter(IPromotion, IObjectCreatedEvent)
def handlerCreatedPromotion(self, event):
    annotations = IAnnotations(self)
    if KEY not in annotations:
        annotations[KEY] = PersistentDict({'evaluations': PersistentDict()})


@adapter(IPromotion, IObjectAddedEvent)
def handlerAddedPromotion(self, event):
    tempdir = tempfile.mkdtemp()
    try:
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
        file_path = os.path.join(tempdir, 'report.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.report.data)
        file_os.close()
        os.system("cd {0}; gs -o report.png -sDEVICE=pngalpha -dLastPage=1 {1}".format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'report.png')
        thumb_file = open(image_path, 'r')

        self.thumbreport = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'report.png'
        )
    except:
        self.thumbreport = None


    try:
        file_path = os.path.join(tempdir, 'letter.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.letter.data)
        file_os.close()
        os.system("cd {0}; gs -o letter.png -sDEVICE=pngalpha -dLastPage=1 {1}".format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'letter.png')
        thumb_file = open(image_path, 'r')

        self.thumbletter = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'letter.png'
        )
    except:
        self.thumbletter = None

    try:
        file_path = os.path.join(tempdir, 'plan.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.plan.data)
        file_os.close()
        os.system("cd {0}; gs -o plan.png -sDEVICE=pngalpha -dLastPage=1 {1}".format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'plan.png')
        thumb_file = open(image_path, 'r')

        self.thumbplan = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'plan.png'
        )
    except:
        self.thumbplan = None

    try:
        shutil.rmtree(tempdir)  # remove tempdir
    except:
        pass



@adapter(IPromotion, IObjectModifiedEvent)
def handlerModifiedPromotion(self, event):

    tempdir = tempfile.mkdtemp()
    try:
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
        file_path = os.path.join(tempdir, 'report.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.report.data)
        file_os.close()
        os.system("cd {0}; gs -o report.png -sDEVICE=pngalpha -dLastPage=1 {1}".format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'report.png')
        thumb_file = open(image_path, 'r')

        self.thumbreport = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'report.png'
        )
    except:
        self.thumbreport = None

    try:
        file_path = os.path.join(tempdir, 'letter.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.letter.data)
        file_os.close()
        os.system("cd {0}; gs -o letter.png -sDEVICE=pngalpha -dLastPage=1 {1}".format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'letter.png')
        thumb_file = open(image_path, 'r')

        self.thumbletter = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'letter.png'
        )
    except:
        self.thumbletter = None

    try:
        file_path = os.path.join(tempdir, 'plan.pdf')
        file_os = open(file_path, 'wb')
        file_os.write(self.plan.data)
        file_os.close()
        os.system("cd {0}; gs -o plan.png -sDEVICE=pngalpha -dLastPage=1 {1}".format(tempdir, file_path))
        image_path = os.path.join(tempdir, 'plan.png')
        thumb_file = open(image_path, 'r')

        self.thumbplan = namedfile.NamedBlobImage(
            data=thumb_file.read(),
            contentType='image/png',
            filename=u'plan.png'
        )
    except:
        self.thumbplan = None


    try:
        shutil.rmtree(tempdir)  # remove tempdir
    except:
        pass
