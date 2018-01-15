# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from plone import api
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form.interfaces import IEditForm


class ICollectiveJudgmentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


# IEvaluable is the marker interface for contentypes who support this behavoir
class IEvaluable(Interface):
    pass


# behaviors interface. When doing IEvaluation(object), you receive an adapter
class IEvaluation(model.Schema):
    directives.omitted('evaluations')
    directives.omitted('voted')
    if api.env.debug_mode():
        directives.no_omit(IEditForm, 'evaluations')
        directives.no_omit(IEditForm, 'voted')

    fieldset(
        'debug',
        label=u'debug',
        fields=('evaluations', 'voted')
    )

    evaluations = schema.Dict(
        title=u'Vote info',
        key_type=schema.TextLine(title=u'voted number'),
        value_type=schema.Int(title=u'Voted so often'),
        required=False)

    voted = schema.List(
        title=u'Vote hashes',
        value_type=schema.TextLine(),
        required=False)

    def vote(request):
        """
        Store the vote information, store the request hash to ensure
        that the user does not vote twice
        """

    def average_vote():
        """
        Return the average voting for an item
        """

    def has_evaluations():
        """
        Return whether anybody ever voted for this item
        """

    def already_voted(request):
        """
        Return the information wether a person already voted.
        This is not very high level and can be tricked out easily
        """

    def clear():
        """
        Clear the evaluations. Should only be called by admins
        """


alsoProvides(IEvaluation, IFormFieldProvider)
