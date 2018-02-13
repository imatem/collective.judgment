# -*- coding: utf-8 -*-
from collective.judgment import _
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant

import datetime


class IAnnualEvaluation(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Tenure
    """

    directives.order_after(evaluation_date='IPersonalData.current_position')
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


@implementer(IAnnualEvaluation)
class AnnualEvaluation(Container):
    """
    """