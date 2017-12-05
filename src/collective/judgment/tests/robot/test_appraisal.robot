# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.judgment -t test_appraisal.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.judgment.testing.COLLECTIVE_JUDGMENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_appraisal.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a appraisal
  Given a logged-in site administrator
    and an add appraisal form
   When I type 'My Appraisal' into the title field
    and I submit the form
   Then a appraisal with the title 'My Appraisal' has been created

Scenario: As a site administrator I can view a appraisal
  Given a logged-in site administrator
    and a appraisal 'My Appraisal'
   When I go to the appraisal view
   Then I can see the appraisal title 'My Appraisal'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add appraisal form
  Go To  ${PLONE_URL}/++add++appraisal

a appraisal 'My Appraisal'
  Create content  type=appraisal  id=my-appraisal  title=My Appraisal


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the appraisal view
  Go To  ${PLONE_URL}/my-appraisal
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a appraisal with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the appraisal title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
