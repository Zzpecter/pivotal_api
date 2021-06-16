@api
Feature: API Pivotal service
  As an application developer,
  I want to get answers for via a REST API,
  So that my app can get answers anywhere.

  @pivotal @fixture_create_projects @fixture_delete_projects
  Scenario: Get all iterations
    Given the "GET" request to "/projects/<projects_id>/iterations" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | length            | 2                   |

  @pivotal @fixture_create_projects @fixture_delete_projects
  Scenario: Get an iteration
    Given the "GET" request to "/projects/<projects_id>/iterations/1" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | length            | 2                   |


  @pivotal @fixture_create_projects @fixture_delete_projects
  Scenario: PUT iteration's information
    Given the following body parameters:
      | key               | value               |
      | length            | 4                   |
    When the "PUT" request to "/projects/<projects_id>/iteration_overrides/1" is sent
    Then the response status code should be 200
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | length            | 4                   |

  @pivotal @fixture_create_projects @fixture_delete_projects
  Scenario: Get the analytics of an iteration
    Given the "GET" request to "/projects/<projects_id>/iterations/1/analytics" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | kind              | analytics           |

  @pivotal @fixture_create_projects @fixture_delete_projects
  Scenario: Get time details of an iteration
    Given the "GET" request to "/projects/<projects_id>/iterations/1/analytics/cycle_time_details" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | kind              | cycle_time_details  |