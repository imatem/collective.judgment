# -*- coding: utf-8 -*-
from collective.judgment import _
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IDexterityFTI
from plone.supermodel import model
from zope import schema
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.i18n import translate

import datetime


class IPromotion(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Promotion
    """

    # directives.widget(level=RadioFieldWidget)
    directives.order_after(requestedposition='IPersonalData.current_position')
    requestedposition = schema.Choice(
        title=_(u'Requested position'),
        vocabulary='collective.judgment.PositionsVocabulary',
        required=True
    )
    directives.order_after(evaluation_date='requestedposition')
    evaluation_date = schema.Date(
        title=_(u'Evaluation Date'),
        required=True,
    )

    @invariant
    def validate_dates(data):
        try:
            really_creation_date = data.__context__.creation_date
            creation_date = datetime.datetime(
                really_creation_date.year(),
                really_creation_date.month(),
                really_creation_date.day(),
                really_creation_date.hour(),
                really_creation_date.minute()
            )
        except Exception:
            creation_date = datetime.datetime.today()

        if (data.evaluation_date < creation_date.date()):
            raise Invalid(
                _('label_error_dates',
                  default=u'The Evaluation Date must be grather than Creation Date')
            )

    @invariant
    def validate_orderpositions(data):
        pvalue = {
            'IAC': 1,
            'ITA': 2,
            'ITB': 3,
            'ITC': 4,
            'TAAA': 5,
            'TAAB': 6,
            'TAAC': 7,
            'TATA': 8,
            'TATB': 9,
            'TATC': 10,
        }
        rposition = pvalue.get(data.requestedposition, 0)

        try:
            apositionvalue = data.__context__.REQUEST.form.get('form.widgets.IPersonalData.current_position', '')
        except Exception:
            apositionvalue = ''

        aposition = 0
        if apositionvalue:
            aposition = pvalue.get(data.__context__.REQUEST.form['form.widgets.IPersonalData.current_position'][0], 0)
        if aposition >= rposition:
            raise Invalid(
                _('label_error_orderpositions',
                  default=u'The Requested Position must be grather than Position')
            )


@implementer(IPromotion)
class Promotion(Container):
    """
    """

    def computedtitle(self):
        # if hasattr(self, 'first_names') and hasattr(self, 'surname'):
        #     return self.first_names + ' ' + self.surname
        # else:
        #     return ''
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        ftititle = translate(
            fti.title,
            domain='collective.judgment',
            target_language='es'
        )
        return ' '.join([ftititle, self.first_name, self.last_name])

    @property
    def Title(self):
        return self.computedtitle
