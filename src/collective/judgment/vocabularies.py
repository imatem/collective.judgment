# -*- coding: utf-8 -*-
from collective.judgment import _
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def YesorNoVocabulary(context):
    items = [
        (_(u'No'), 'no'),
        (_(u'Yes'), 'yes'),
    ]

    items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
    return SimpleVocabulary(items)
directlyProvides(YesorNoVocabulary, IVocabularyFactory)
