# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ITenure(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Tenure
    """


@implementer(ITenure)
class Tenure(Container):
    """
    """
