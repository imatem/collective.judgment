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


class ICollectiveJudgmentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


# Ivotable is the marker interface for contentypes who support this behavoir
class Ivotable(Interface):
    pass


# behaviors interface. When doing Ivoting(object), you receive an adapter
class IVoting(model.Schema):
    if not api.env.debug_mode():
        directives.omitted('votes')
        directives.omitted('voted')

    fieldset(
        'debug',
        label=u'debug',
        fields=('votes', 'voted')
    )

    votes = schema.Dict(
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

    def has_votes():
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
        Clear the votes. Should only be called by admins
        """


alsoProvides(IVoting, IFormFieldProvider)
