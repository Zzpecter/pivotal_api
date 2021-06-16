@api
Feature: API Pivotal service
  As an application developer,
  I want to get answers for via a REST API,
  So that my app can get answers anywhere.

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Get all epics
    When the "GET" request to "/projects/<projects_id>/epics" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | AUTO_NEW_EPIC       |

  @pivotal @fixture_create_projects @fixture_delete_projects
  Scenario: Post an epic to project
    Given the following body parameters:
      | key               | value               |
      | name              | AUTO_NEW_EPIC       |
    When the "POST" request to "/projects/<projects_id>/epics" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | AUTO_NEW_EPIC       |

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Get an epic from project
    When the "GET" request to "/projects/<projects_id>/epics/<epics_id>" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | AUTO_NEW_EPIC       |

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Put an epic to project
    Given the following body parameters:
      | key               | value                |
      | name              | AUTO_UPDATED_EPIC    |
    When the "PUT" request to "/projects/<projects_id>/epics/<epics_id>" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | AUTO_UPDATED_EPIC   |

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Delete an epic from project
    When the "DELETE" request to "/projects/<projects_id>/epics/<epics_id>" is sent
    Then the response status code should be 204
    Then the "GET" request to "/projects/<projects_id>/epics/<epics_id>" is sent
    And the response status code should be 404

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Get an epic
    When the "GET" request to "/epics/<epics_id>" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | AUTO_NEW_EPIC       |