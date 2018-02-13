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


def ClassificationsVocabulary(context):
    items = [
        (_(u'Researcher'), 'researcher'),
        (_(u'Academic Technician'), 'academictec'),
    ]

    items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
    return SimpleVocabulary(items)


directlyProvides(ClassificationsVocabulary, IVocabularyFactory)


def PositionsVocabulary(context):
    """Vocabulary for position."""
    items = [
        ('IAC', u'Investigador Asociado C'),
        ('ITA', u'Investigador Titular A'),
        ('ITB', u'Investigador Titular B'),
        ('ITC', u'Investigador Titular C'),
        ('TAAA', u'Técnico Académico Asociado A'),
        ('TAAB', u'Técnico Académico Asociado B'),
        ('TAAC', u'Técnico Académico Asociado C'),
        ('TATA', u'Técnico Académico Titular A'),
        ('TATB', u'Técnico Académico Titular B'),
        ('TATC', u'Técnico Académico Titular C'),
    ]
    items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
    return SimpleVocabulary(items)


directlyProvides(PositionsVocabulary, IVocabularyFactory)
