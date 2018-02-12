# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IRehiring(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Tenure
    """


@implementer(IRehiring)
class Rehiring(Container):
    """
    """
