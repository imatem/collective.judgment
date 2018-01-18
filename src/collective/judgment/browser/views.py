# -*- coding: utf-8 -*-
from collective.judgment.interfaces import IEvaluation
from plone import api
from plone.dexterity.browser.view import DefaultView
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from smtplib import SMTPRecipientsRefused


class PromotionView(DefaultView):
    """ The default view for talks
    """

    def foo(self):
        return ''


class FolderCdimView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        form = self.request.form
        if form:
            formkeys = form.keys()
            if 'send_email' in formkeys:
                self.send_email()
        return self.index()

    def itembrains(self):

        option = 'pending'
        if self.request.form:
            option = self.request.form.get('options', 'pending')

        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(
            path=dict(query='/'.join(self.context.getPhysicalPath()), depth=1),
            review_state=option,
            # sort_on='start'
        )

        return brains

    def evaluations(self, brain):

        values = IEvaluation(brain.getObject()).evaluations

        evaluators = []

        isManager = self.isManager()
        userid = api.user.get_current().id

        for gmember in api.user.get_users(groupname='evaluators'):
            if isManager:
                evaluators.append((gmember.getProperty('fullname'), values.get(gmember.id, None), gmember.id))
            elif userid == gmember.id:
                evaluators.append((gmember.getProperty('fullname'), values.get(gmember.id, None), gmember.id))
                break
        return evaluators

    def isManager(self):

        local_roles = self.context.portal_membership.getAuthenticatedMember().getRolesInContext(self.context)
        if 'Manager' in local_roles or 'Reviewer' in local_roles:
            return True
        return False

    def send_email(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(
            path=dict(query='/'.join(self.context.getPhysicalPath()), depth=1),
            review_state='pending',
            # sort_on='start'
        )

        evaluators = api.user.get_users(groupname='evaluators')
        emails = {}

        for brain in brains:
            values = IEvaluation(brain.getObject()).evaluations
            for gmember in evaluators:
                if values.get(gmember.id, None) is None:
                    emails.setdefault(gmember.id, [])
                    emails[gmember.id].append((brain.Title, brain.getURL()))

        evaluators_data = {}
        for evaluator in evaluators:
            evaluators_data[evaluator.id] = {
                'name': evaluator.getProperty('fullname'),
                'email': evaluator.getProperty('email'),
            }

        message = []
        for k, v in emails.iteritems():
            mail_text = 'Dear %s:' % (evaluators_data[k]['name'])
            if len(v) > 1:
                mail_text += u'\n Please evaluate the next cases: \n'
            else:
                mail_text += u'\n Please evaluate the next case: \n'
            for item in v:
                mail_text += (item[0] + ' ' + item[1]).decode('utf-8')
                mail_text += u'\n'
            mail_text += u'.\n\n\n\n'
            mail_text += u' Best regards, \n'
            mail_text += u'Commissioner \n'

            try:
                api.portal.send_email(
                    recipient=evaluators_data[k]['email'],
                    sender='apoyo@im.unam.mx',
                    subject='Evaluators System',
                    body=mail_text,
                )
                message.append(evaluators_data[k]['email'])
            except SMTPRecipientsRefused:
                # Don't disclose email address on failure
                raise SMTPRecipientsRefused('Recipient address rejected by server')

        IStatusMessage(self.request).addStatusMessage(
            'The system sended email to: ' + ', '.join(message), "info"
        )
        return True
