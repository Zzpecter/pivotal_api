@api
Feature: Pivotal API Service
  As an application developer,
  I want to get responses from a REST API,
  So that my app can consume those responses.


  @pivotal @service @get_projects @cache_clear
  Scenario: Get Projects
    Given the "GET" request to "/projects" is sent
    Then the response status code should be 200

  @pivotal @service @get_project @fixture_create_projects @fixture_delete_projects
  Scenario: Get Project
    When the "GET" request to "/projects/<id>" is sent
    Then the response status code should be 200

  @pivotal @service @post_project @fixture_delete_projects
  Scenario: Post Project
    Given the following request body parameters:
      | key               | value               |
      | name              | BDD-Test-Project    |
      | iteration_length  | 2                   |
      | week_start_day    | Monday              |
    When the "POST" request to "/projects" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | BDD-Test-Project    |
      | iteration_length  | 2                   |
      | week_start_day    | Monday              |
    And the response schema should be verified with "schema_projects.json"


  @pivotal @service @put_project @fixture_create_projects @fixture_delete_projects
  Scenario: Put Project
    Given the following request body parameters:
      | key               | value               |
      | name              | BDD-Update-Project  |
      | iteration_length  | 3                   |
      | week_start_day    | Saturday            |
    When the "PUT" request to "/projects/<id>" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | BDD-Update-Project  |
      | iteration_length  | 3                   |
      | week_start_day    | Saturday            |

  @pivotal @service @del_project @fixture_create_projects
  Scenario: Delete Project
    When the "DELETE" request to "/projects/<id>" is sent
    Then the response status code should be 204