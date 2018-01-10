# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.judgment -t test_tenure.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.judgment.testing.COLLECTIVE_JUDGMENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_tenure.robot
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

Scenario: As a site administrator I can add a tenure
  Given a logged-in site administrator
    and an add tenure form
   When I type 'My Tenure' into the title field
    and I submit the form
   Then a tenure with the title 'My Tenure' has been created

Scenario: As a site administrator I can view a tenure
  Given a logged-in site administrator
    and a tenure 'My Tenure'
   When I go to the tenure view
   Then I can see the tenure title 'My Tenure'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add tenure form
  Go To  ${PLONE_URL}/++add++tenure

a tenure 'My Tenure'
  Create content  type=tenure  id=my-tenure  title=My Tenure


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the tenure view
  Go To  ${PLONE_URL}/my-tenure
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a tenure with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the tenure title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
