# -*- coding: utf-8 -*-

from plone import api
from zope.globalrequest import getRequest


def logged_in_handler(event):
    """
    Listen to the event and perform the action accordingly.
    """
    url = api.portal.get().absolute_url()
    request = getRequest()
    if request is None:
        # HTTP request is not present e.g.
        # when doing unit testing / calling scripts from command line
        return

    # check if came_from is not empty, then clear it up, otherwise further
    # Plone scripts will override our redirect
    if request.get('came_from', None):
        request['came_from'] = ''
        request.form['came_from'] = ''
    request.RESPONSE.redirect(url)
