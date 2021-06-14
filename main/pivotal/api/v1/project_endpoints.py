"""
Send HTTP requests to the Project Endpoints of the Pivotal API

Classes:

    ProjectEndpoints

Functions:

    get_projects -> response
    get_project(id) -> response
    post_project(data) -> response
    put_project(id, data) -> response
    delete_project(id) -> response

"""
from main.core.request_controller import RequestController
from main.pivotal.utils.api_constants import HttpMethods as http
from main.pivotal.utils.api_constants import Endpoints as endpoints


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

        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.GET.value,
                         endpoints.PROJECTS.value
                         )

    @staticmethod
    def get_project(project_id):
        """
        Gets a specific project from the user

       Args:
            project_id(int): the id of the project to be created
        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.GET.value,
                         f"/{endpoints.PROJECTS.value}{project_id}")

    @staticmethod
    def post_project(payload_dict):
        """
        Posts a new project

       Args:
            payload_dict(dict):the data to create
        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.POST.value,
                         endpoints.PROJECTS.value,
                         payload=payload_dict)

    @staticmethod
    def put_project(project_id, payload_dict):
        """
        Updates a specific project

       Args:
            project_id(int): the id of the project to be deleted
            payload_dict(dict):the data to update
        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.PUT.value,
                         f"/{endpoints.PROJECTS.value}{project_id}",
                         payload=payload_dict)

    @staticmethod
    def delete_project(project_id):
        """
        Deletes a specific project

       Args:
            project_id(int): the id of the project to be deleted
        Returns:
            response(object): the response object
        """
        return RequestController.get_instance().\
            send_request(http.DELETE.value,
                         f"/{endpoints.PROJECTS.value}{project_id}")
