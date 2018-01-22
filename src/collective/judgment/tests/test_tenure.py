# -*- coding: utf-8 -*-
from collective.judgment.content.tenure import ITenure
from collective.judgment.testing import COLLECTIVE_JUDGMENT_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class TenureIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_JUDGMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='tenure')
        schema = fti.lookupSchema()
        self.assertEqual(ITenure, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='tenure')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='tenure')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(ITenure.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='tenure',
            id='tenure',
        )
        self.assertTrue(ITenure.providedBy(obj))
