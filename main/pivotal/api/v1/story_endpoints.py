"""
Send HTTP requests to the Story Endpoints of the Pivotal API

Classes:

    StoryEndpoints

Functions:

    get_stories
    get_stories(id)
    post_story(data)
    put_story(id, data)
    delete_story(id)

Misc variables:

    my_request_controller
"""
from main.core.request_controller import RequestController

my_request_controller = RequestController()


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

        Returns
        ----------
            response : object
                the response object, loaded with the list of projects.
        """
        return my_request_controller.\
            send_request('GET',
                         f"/projects/{project_id}/stories/")

    @staticmethod
    def get_story(project_id, story_id):
        """
        Gets a specific story from the project

        Returns
        ----------
            response : object
                the response object, loaded with the selected project's data.
        """
        return my_request_controller.\
            send_request('GET',
                         f"/projects/{project_id}/stories/{story_id}")

    @staticmethod
    def post_story(payload_dict):
        """
        Posts a new story

        Parameters
        ----------
            payload_dict : dict
                The data to be sent, encoded in a dictionary
        Returns
        ----------
            response : object
                the response object.
        """
        return my_request_controller.\
            send_request('POST',
                         '/projects/{project_id}/stories',
                         payload=payload_dict)

    @staticmethod
    def put_story(project_id, story_id, payload_dict):
        """
        Updates a specific story

        Parameters
        ----------
            project_id : int
                the id of the project to be updated
            story_id : int
                the id of the project to be updated
            payload_dict : dict
                The data to be sent, encoded in a dictionary
        Returns
        ----------
            response : object
                the response object.
        """
        return my_request_controller.\
            send_request('PUT',
                         f'/projects/{project_id}/stories/{story_id}',
                         payload=payload_dict)

    @staticmethod
    def delete_story(project_id, story_id):
        """
        Deletes a specific story

        Parameters
        ----------
            project_id : int
                the id of the project to be deleted
            story_id : int
                the id of the project to be deleted
        Returns
        ----------
            response : object
                the response object.
        """
        return my_request_controller.\
            send_request('DELETE',
                         f'/projects/{project_id}/stories/{story_id}')
