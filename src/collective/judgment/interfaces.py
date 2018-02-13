# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveJudgmentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


# IEvaluable is the marker interface for contentypes who support this behavoir
class IEvaluable(Interface):
    pass


# behaviors interface. When doing IEvaluation(object), you receive an adapter
class IEvaluation(model.Schema):
    directives.omitted('evaluations')
    # show debug tab
    # from plone import api
    # if api.env.debug_mode():
    #     directives.no_omit(IEditForm, 'evaluations')

    fieldset(
        'debug',
        label=u'debug',
        fields=('evaluations', )
    )

    evaluations = schema.Dict(
        title=u'Evaluation info',
        key_type=schema.TextLine(title=u'User ID'),
        value_type=schema.TextLine(title=u'Evaluation'),
        required=False)

    def evaluate(evaluation, userid):
        """
        Store the evaluation information, store the user id to ensure
        that the user does not vote twice
        """

    def already_evaluated(userid):
        """
        Return the information wether a person already evaluated.
        """

    def clear():
        """
        Clear the evaluations. Should only be called by admins
        """


alsoProvides(IEvaluation, IFormFieldProvider)
