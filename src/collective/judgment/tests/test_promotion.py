# -*- coding: utf-8 -*-
from collective.judgment.content.promotion import IPromotion
from collective.judgment.testing import COLLECTIVE_JUDGMENT_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PromotionIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_JUDGMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='promotion')
        schema = fti.lookupSchema()
        self.assertEqual(IPromotion, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='promotion')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='promotion')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IPromotion.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='promotion',
            id='promotion',
        )
        self.assertTrue(IPromotion.providedBy(obj))
