@api
Feature: Pivotal API Stories Service
  As an application developer,
  I want to query the Stories of the Pivotal API,
  So that my app can consume those responses.


  @pivotal @service @fixture_create_projects @get_stories @fixture_delete_stories
  Scenario: Get Stories
    Given the "GET" request to "/projects/<project_id>/stories" is sent
    Then the response status code should be 200

  @pivotal @service @get_story @fixture_create_projects @fixture_create_stories @fixture_delete_stories
  Scenario: Get Story
    When the "GET" request to "/projects/<project_id>/stories/<story_id>" is sent
    Then the response status code should be 200

  @pivotal @service @post_story @fixture_create_projects @fixture_delete_stories
  Scenario: Post Story
    Given the following request body parameters:
      | key               | value               |
      | name              | AUTO_TEST_STORY     |
      | description       | default payload     |
      | story_type        | feature             |
    When the "POST" request to "/projects/<project_id>/stories" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | AUTO_TEST_STORY     |
      | description       | default payload     |
      | story_type        | feature             |
    And the response schema should be verified with "schema_stories.json"


  @pivotal @service @put_story @fixture_create_projects @fixture_create_stories @fixture_delete_projects
  Scenario: Put Story
    Given the following request body parameters:
      | key               | value               |
      | name              | AUTO_UPDATED_STORY  |
      | description       | updated payload     |
      | story_type        | feature             |
    When the "PUT" request to "/projects/<project_id>/stories/<story_id>" is sent
    Then the response status code should be 200
    And the response body should be verified with:
      | key               | value               |
      | name              | AUTO_UPDATED_STORY  |
      | description       | updated payload     |
      | story_type        | feature             |

  @pivotal @service @del_story @fixture_create_projects @fixture_create_stories @fixture_delete_projects
  Scenario: Delete Story
    When the "DELETE" request to "/projects/<project_id>/stories/<story_id>" is sent
    Then the response status code should be 204