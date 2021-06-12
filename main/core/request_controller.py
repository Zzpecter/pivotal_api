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
from assertpy import assert_that

from main.core.utils.file_reader import read_json
from main.core.utils.logger import CustomLogger


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
    log_response() :
        generates a report based on the HTTP response and saves it with
        the logger

    """
    def __init__(self, config_path=r'main\pivotal\resources\config.json'):
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
        if request_method in 'PUT' or request_method in 'POST':
            self.response = requests.request(request_method,
                                             url=f'{self.url}{endpoint}',
                                             data=json.dumps(payload),
                                             headers=self.header)
        else:
            self.response = requests.request(request_method,
                                             url=f'{self.url}{endpoint}',
                                             headers=self.header)

        try:
            assert_that(self.response.status_code).is_equal_to(HTTPStatus.OK)
        except AssertionError as error:
            self.logger.warning(f"{error}")

        self.log_response()
        if self.response.status_code is not HTTPStatus.OK.value:
            return self.response.status_code, {"message": self.response.text}
        return self.response.status_code, self.response.json()

    def log_response(self):
        """
        Generates a report based on the HTTP response and saves it with the
        logger.
        """
        if self.response is not None:
            aux_string = '.... :::: PRINTING THE RESPONSE REPORT :::: ....\n'
            aux_string += f'  - METHOD USED: {self.last_method_used} \n'
            aux_string += f'  - url: {self.response.url} \n'
            aux_string += f'  - STATUS CODE: {self.response.status_code} - ' \
                          f' {self.response.reason} \n'
            aux_string += f'  - TIME ELAPSED: {self.response.elapsed} \n'
            aux_string += '.... :::: COMPLETE JSON RESPONSE :::: ....\n'
            self.logger.info(aux_string)
            if self.response.status_code == 200:
                self.logger.info(json.dumps(self.response.json(), indent=4,
                                            sort_keys=True))
            self.logger.info('\n.... ::::  REPORT COMPLETED :::: ....\n\n ')
        else:
            self.logger.warning('No response available')
