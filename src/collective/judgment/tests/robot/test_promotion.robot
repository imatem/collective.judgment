# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.judgment -t test_promotion.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.judgment.testing.COLLECTIVE_JUDGMENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_promotion.robot
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

Scenario: As a site administrator I can add a promotion
  Given a logged-in site administrator
    and an add promotion form
   When I type 'My Promotion' into the title field
    and I submit the form
   Then a promotion with the title 'My Promotion' has been created

Scenario: As a site administrator I can view a promotion
  Given a logged-in site administrator
    and a promotion 'My Promotion'
   When I go to the promotion view
   Then I can see the promotion title 'My Promotion'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add promotion form
  Go To  ${PLONE_URL}/++add++promotion

a promotion 'My Promotion'
  Create content  type=promotion  id=my-promotion  title=My Promotion


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the promotion view
  Go To  ${PLONE_URL}/my-promotion
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a promotion with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the promotion title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
