"""
Send HTTP requests to the Story Endpoints of the Pivotal API

Classes:

    StoryEndpoints

Functions:

    get_stories -> response
    get_stories(id) -> response
    post_story(data) -> response
    put_story(id, data) -> response
    delete_story(id) -> response

"""
from main.core.request_controller import RequestController
from main.pivotal.utils.api_constants import HttpMethods as http
from main.pivotal.utils.api_constants import Endpoints as endpoints


class StoryEndpoints:
    """
        Static lass for implementing the endpoints of pivotal stories

        ...

        Methods
        -------
        get_stories()
            get all stories
        get_story(id)
            get a story with specific id
        post_story(data)
            post a new story
        put_story(id, data)
            update an existing story
        delete_story(id)
            deletes a specific story
        """

    @staticmethod
    def get_stories(project_id):
        """
        Gets all stories from the project
        Args:
            project_id(int): the id of the
            project to be retrieved
        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.GET.value,
                         f'/{endpoints.PROJECTS.value}{project_id}/'
                         f'{endpoints.STORIES.value}')

    @staticmethod
    def get_story(project_id, story_id):
        """
        Gets a specific story from the project
        Args:
            project_id(int): the id of the
            project to be retrieved
            story_id(int): the id of the
            story to be retrieved

        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.GET.value,
                         f'/{endpoints.PROJECTS.value}{project_id}/'
                         f'{endpoints.STORIES.value}{story_id}')

    @staticmethod
    def post_story(project_id, payload_dict):
        """
        Posts a new story
        Args:
            project_id(int): the id of the project to be updated
            payload_dict(dict): the data to create

        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.POST.value,
                         f'/{endpoints.PROJECTS.value}{project_id}/'
                         f'{endpoints.STORIES.value}',
                         payload=payload_dict)

    @staticmethod
    def put_story(project_id, story_id, payload_dict):
        """
        Updates a selected story
        Args:
            project_id(int): the id of the project to be updated
            story_id(int): the id of the story to be updated
            payload_dict(dict): the data to update

        Returns:
            response(object): the response object

        """
        return RequestController.get_instance().\
            send_request(http.PUT.value,
                         f'/{endpoints.PROJECTS.value}{project_id}/'
                         f'{endpoints.STORIES.value}{story_id}',
                         payload=payload_dict)

    @staticmethod
    def delete_story(project_id, story_id):
        """
        Deletes a specific story

       Args:
            project_id(int): the id of the project to be updated
            story_id(int): the id of the story to be deleted
        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.DELETE.value,
                         f'/{endpoints.PROJECTS.value}{project_id}/'
                         f'{endpoints.STORIES.value}{story_id}')
