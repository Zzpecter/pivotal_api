"""
Send HTTP requests to the Project Endpoints of the Pivotal API

Classes:

    ProjectEndpoints

Functions:

    get_projects
    get_project(id)
    post_project(data)
    put_project(id, data)
    delete_project(id)

Misc variables:

    my_request_controller
"""
from main.core.request_controller import RequestController

my_request_controller = RequestController()


class ProjectEndpoints:
    """
    Static lass for implementing the endpoints of pivotal projects

    ...

    Methods
    -------
    get_projects()
        get all projects
    get_project(id)
        get a project with specific id
    post_project(data)
        post a new project
    put_project(id, data)
        update an existing project
    delete_project(id)
        deletes a specific project
    """

    @staticmethod
    def get_projects():
        """
        Gets all projects from the user

        Returns
        ----------
            response : object
                the response object, loaded with the list of projects.
        """
        return my_request_controller.\
            send_request('GET',
                         "/projects/")

    @staticmethod
    def get_project(project_id):
        """
        Gets a specific project from the user

        Returns
        ----------
            response : object
                the response object, loaded with the selected project's data.
        """
        return my_request_controller.\
            send_request('GET',
                         f"/projects/{project_id}")

    @staticmethod
    def post_project(payload_dict):
        """
        Posts a new project

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
                         '/projects/',
                         payload=payload_dict)

    @staticmethod
    def put_project(project_id, payload_dict):
        """
        Updates a specific project

        Parameters
        ----------
            project_id : int
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
                         f'/projects/{project_id}',
                         payload=payload_dict)

    @staticmethod
    def delete_project(project_id):
        """
        Deletes a specific project

        Parameters
        ----------
            project_id : int
                the id of the project to be updated
        Returns
        ----------
            response : object
                the response object.
        """
        return my_request_controller.\
            send_request('DELETE',
                         f'/projects/{project_id}')
