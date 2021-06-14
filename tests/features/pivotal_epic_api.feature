@api
Feature: API Pivotal service
  As an application developer,
  I want to get answers for via a REST API,
  So that my app can get answers anywhere.

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Get all epics of a project
    Given the "GET" request to "/projects/<projects_id>/epics" is sent
    Then the response status code should be 200

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Post a new epic
    Given the following body parameters:
      | key               | value               |
      | name              | New epic :D         |
    When the "POST" request to "/projects/<projects_id>/epics" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | New epic :D         |

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Get a specific epic of a project
    Given the "GET" request to "/projects/<projects_id>/epics/<epics_id>" is sent
    Then the response status code should be 200

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Put updates a specific epic of a project
    Given the following body parameters:
      | key               | value                |
      | name              | Updated epic :D      |
    When the "PUT" request to "/projects/<projects_id>/epics/<epics_id>" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | Updated epic :D     |

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Delete a specific epic of a project
    Given the "DELETE" request to "/projects/<projects_id>/epics/<epics_id>" is sent
    Then the response status code should be 204

  @pivotal @fixture_create_epics @fixture_delete_projects
  Scenario: Get an individual epic
    Given the "GET" request to "/epics/<epics_id>" is sent
    Then the response status code should be 200






