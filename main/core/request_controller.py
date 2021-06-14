"""
Create and send HTTP requests implementing this module

Classes:

    RequestController

Functions:

    send_request(request_method, endpoint, payload) -> object
    log_response()

Misc variables:

    url
    header
    last_method_used
"""

from http import HTTPStatus
import json
import requests
from requests import Session
from assertpy import assert_that
from main.core.utils.file_reader import read_json
from main.core.utils.logger import CustomLogger
from main.pivotal.utils.api_constants import CONFIG_PATH


class RequestController:
    """
    A class to abstract HTTP requests, designed to support configurations
    to connect to multiple API's

    ...

    Attributes
    ----------
    config_path : str
        the application-based path to the configuration to be loaded to
        the RequestController

    Methods
    -------
    send_request(request_method, endpoint, payload:Optional):
        sends an HTTP request via the pre-configured Request Controller
    close_session():
        closes the request_controller session

    """
    __instance = None

    def __init__(self, config_path=CONFIG_PATH):
        """
        Constructs all the necessary attributes for the Request Controller
        object.

        Parameters
        ----------
            config_path : str
                the application-based path to the config file for the API to
                be used
        """
        self.json_config = read_json(config_path)
        self.url = self.json_config['API_URL']

        self.header = {'Content-type': self.json_config['CONTENT_TYPE'],
                       self.json_config['API_TOKEN_NAME']:
                       self.json_config['API_TOKEN']}

        self.response = None
        self.last_method_used = None
        self.logger = CustomLogger(name='api-logger')
        self.logger.debug('Logger initialized!')
        self.session = Session()

    @staticmethod
    def get_instance():
        """This method gets a singleton instance of the RequestsManager class.

        Returns:
            RequestManager -- return a instance of RequestsManager class.
        """
        if RequestController.__instance is None:
            RequestController.__instance = RequestController()
        return RequestController.__instance

    def return_json(self):
        try:
            self.response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)

        json_obj = self.response.json()
        return json_obj

    def send_request(self, request_method, endpoint, payload=None):
        """
        Constructs all the necessary attributes for the Request
        Controller object.

        Parameters
        ----------
            request_method : str
                The HTTP method to be used in the request
            endpoint : str
                the path to the API endpoint that the request will be accessing
            payload : dict
                the optional payload data for sending as json with the request

        Returns
        ----------
            response : object
                the response object, sent back as a result from the HTTP
                request performed
        """
        self.last_method_used = request_method
        if request_method in ['PUT', 'POST']:
            self.response = requests.request(request_method,
                                             url=f'{self.url}{endpoint}',
                                             data=json.dumps(payload),
                                             headers=self.header)
        else:
            self.response = requests.request(request_method,
                                             url=f'{self.url}{endpoint}',
                                             headers=self.header)

        self.logger.info(f'  - METHOD USED: {self.last_method_used}')
        self.logger.info(f'  - URL: {self.response.url}')
        self.logger.info(f'  - STATUS CODE: {self.response.status_code} '
                         f'- {self.response.reason}')
        self.logger.info(f'  - TIME ELAPSED: {self.response.elapsed} \n')

        return self.response.status_code, self.response

    def close_session(self):
        """Close Session"""
        self.session.close()


