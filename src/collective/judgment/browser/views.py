# -*- coding: utf-8 -*-
from collections import OrderedDict
from collective.judgment import _
from collective.judgment.interfaces import IEvaluation
from plone import api
from plone.dexterity.browser.view import DefaultView
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from smtplib import SMTPRecipientsRefused
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory

import datetime


class PromotionView(DefaultView):
    """ The default view for talks
    """

    def foo(self, element):
        return ''

    def timeleft(self):
        today = datetime.date.today()
        evaluation = self.context.evaluation_date
        timeleft = evaluation - today
        return str(timeleft.days)

    def order_items(self):
        # items = OrderedDict()
        items = []
        others = []

        for item in self.context.items():
            itemportal = item[1].portal_type
            if itemportal == 'Pdf File':
                items.append(item[1])
            else:
                others.append(item[1])

        return {'base': items, 'extra': others}

    def editurl(self):
        return '++add++Pdf File?title=Documentation'


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
            sort_on='evaluation_date'
        )
        return brains

    def evaluations(self, brain):

        evaluations = IEvaluation(brain.getObject()).evaluations
        evaluators = []
        isManager = self.isManager()
        userid = api.user.get_current().id

        for xid in sorted(evaluations.keys()):
            member = api.user.get(username=xid)

            if isManager:
                member_evaluations = evaluations.get(member.id, None)
                value = member_evaluations and member_evaluations[0]['evaluation']
                evaluators.append((member.getProperty('fullname'), value, member.id))
            elif userid == member.id:
                member_evaluations = evaluations.get(member.id, None)
                value = member_evaluations and member_evaluations[0]['evaluation']
                evaluators.append((member.getProperty('fullname'), value, member.id))
                break
        return evaluators

    def isManager(self):

        local_roles = self.context.portal_membership.getAuthenticatedMember().getRolesInContext(self.context)
        if 'Manager' in local_roles or 'Reviewer' in local_roles:
            return True
        return False

    def evaluation_date(self, brain):
        return brain.getObject().evaluation_date

    def position(self, brain):
        position = brain.getObject().current_position
        vocabulary = getUtility(
            IVocabularyFactory,
            'collective.judgment.PositionsVocabulary')(self.context).by_value
        complete_position = vocabulary[position].title
        if brain.portal_type == 'promotion':
            rposition = brain.getObject().requestedposition
            complete_position += ' - ' + vocabulary[rposition].title
        return complete_position

    def downloadDocs(self, brain):
        obj = brain.getObject()

        items = []
        for item in obj.items():
            itemportal = item[1].portal_type
            if itemportal == 'Pdf File':
                items.append(item[1])

        return items

    def title_state(self, brain):

        wft = api.portal.get_tool('portal_workflow')
        obj = brain.getObject()
        current_state = api.content.get_state(obj)
        itemstatus = translate(
            wft.getTitleForStateOnType(current_state, obj.portal_type),
            domain='collective.judgment',
            target_language=self.context.REQUEST.LANGUAGE
        )

        return itemstatus

    def send_email(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(
            path=dict(query='/'.join(self.context.getPhysicalPath()), depth=1),
            review_state='pending',
            sort_on='evaluation_date'
        )

        evaluators = api.user.get_users(groupname='evaluators')
        emails = {}

        for brain in brains:
            values = IEvaluation(brain.getObject()).evaluations
            for gmember in evaluators:
                if len(values.get(gmember.id, [])) == 0:
                    emails.setdefault(gmember.id, [])
                    emails[gmember.id].append((brain.Title, brain.getURL()))


        evaluators_data = {}
        for evaluator in evaluators:
            evaluators_data[evaluator.id] = {
                'name': evaluator.getProperty('fullname'),
                'email': evaluator.getProperty('email'),
            }

        message = []
        for k, v in emails.items():
            salutation = _(u'email_intro_msg', default=u'Dear ${name}', mapping={u'name': safe_unicode(evaluators_data[k]['name'])})
            if len(v) > 1:
                mail_intro = _(u'You have the following pending reviews:')
            else:
                mail_intro = _(u'you have the following pending review:')
            mail_cases = u'\n'.join([i[0] + u' ' + safe_unicode(i[1]) for i in v])
            mail_sign = u'Asuntos Académicos\nInstituto de Matemáticas, UNAM'
            salutation = self.context.translate(salutation)
            mail_intro = self.context.translate(mail_intro)
            mail_text = '\n'.join([salutation, mail_intro, u'\n', mail_cases, u'\n\n', mail_sign])
            mail_subject = self.context.translate(_(u'Pending reviews, IM UNAM'))
            try:
                api.portal.send_email(
                    recipient=evaluators_data[k]['email'],
                    sender='apoyo@im.unam.mx',
                    subject=mail_subject,
                    body=mail_text,
                )
                message.append(evaluators_data[k]['email'])
            except SMTPRecipientsRefused:
                # Don't disclose email address on failure
                raise SMTPRecipientsRefused('Recipient address rejected by server')

        IStatusMessage(self.request).addStatusMessage(
            self.context.translate(_(u'The system sended email to: '))  + ', '.join(message),
            'info'
        )
        return True
