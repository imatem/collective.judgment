# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.judgment


class CollectiveJudgmentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.judgment)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.judgment:default')


COLLECTIVE_JUDGMENT_FIXTURE = CollectiveJudgmentLayer()


COLLECTIVE_JUDGMENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_JUDGMENT_FIXTURE,),
    name='CollectiveJudgmentLayer:IntegrationTesting'
)


COLLECTIVE_JUDGMENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_JUDGMENT_FIXTURE,),
    name='CollectiveJudgmentLayer:FunctionalTesting'
)


COLLECTIVE_JUDGMENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_JUDGMENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveJudgmentLayer:AcceptanceTesting'
)
