# -*- coding: utf-8 -*-
from collective.judgment.behaviors.evaluation import KEY
from collective.judgment.content.files import IPdfFile
from collective.judgment.interfaces import IEvaluable
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from plone import api
from plone import namedfile
from plone.app.dexterity.behaviors import constrains
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

import os
import shutil
import tempfile


@adapter(IEvaluable, IObjectCreatedEvent)
def handlerCreatedPromotion(self, event):
    annotations = IAnnotations(self)
    if KEY not in annotations:
        annotations[KEY] = PersistentDict()
        evaluations = annotations[KEY]
        for member in api.user.get_users(groupname='evaluators'):
            evaluations[member.id] = PersistentList()


@adapter(IEvaluable, IObjectAddedEvent)
def handleAddedEvaluable(obj, event):
    with api.env.adopt_roles(roles='Manager'):
        constraints = ISelectableConstrainTypes(obj)
        constraints.setConstrainTypesMode(constrains.DISABLED)
        document = api.content.create(type='Document', title='Carta', container=obj)
        api.group.grant_roles(groupname='evaluators', roles=['Editor'], obj=document)
        constraints.setLocallyAllowedTypes(['Pdf File'])
        constraints.setImmediatelyAddableTypes(['Pdf File'])
        constraints.setConstrainTypesMode(constrains.ENABLED)

        for member in api.user.get_users(groupname='evaluators'):
            api.user.grant_roles(username=member.id, roles=['Reader'], obj=obj)

        api.content.disable_roles_acquisition(obj=obj)
        api.group.grant_roles(groupname='Reviewers', roles=['Reader'], obj=obj)


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
