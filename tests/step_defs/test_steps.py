"""
This module contains step definitions for pivotal_projects.feature.
"""
from assertpy import assert_that
from pytest_bdd import scenarios, given, when, then, parsers
from sttable import parse_str_table
from jsonschema import validate
from main.core.utils.file_reader import read_json
from main.core.utils.logger import CustomLogger
from main.core.utils.table_parser import TableParser
from main.core.utils.string_utils import StringUtils as str_utils
from main.pivotal.utils.api_constants import HttpMethods as http
from main.core.request_controller import RequestController

LOGGER = CustomLogger('test_logger')


scenarios('../features/pivotal_projects.feature')


@given(parsers.parse('the "{http_method}" request to "{endpoint}" is sent'))
@when(parsers.parse('the "{http_method}" request to "{endpoint}" is sent'))
def step_send_request(http_method, endpoint, request):
    """
    The function that executes the request controller and receives the response
    from the API
    Args:
        http_method (str): http method or verb
        endpoint (str): endpoint used to interact with request manager
        request (request): request fixture object
    """

    tags_to_replace = str_utils.search_text_between_tags(endpoint)

    LOGGER.debug(f'Tags found:  {tags_to_replace}')
    LOGGER.debug(f'un-processed endpoint:  {endpoint}')

    for tag in tags_to_replace:
        LOGGER.debug(f'found id for endpoint: '
                     f'{request.config.cache.get(tag, None)}')
        endpoint = str_utils.replace_string(endpoint,
                                            str(request.config.cache.get(
                                                tag, None)),
                                            f'<{tag}>'
                                            )
        LOGGER.debug(f'WORKING on tags:  {endpoint}')

    LOGGER.debug(f'processed endpoint:  {endpoint}')

    body = request.config.cache.get('body', None)

    status_code, response = RequestController.get_instance().send_request(
            request_method=http_method,
            endpoint=endpoint,
            payload=body)

    LOGGER.info(f'RESPONSE  {response}')
    request.config.cache.set('status_code', status_code)
    if http_method != http.DELETE.value:
        request.config.cache.set('response', response.json())


@given(parsers.parse('the following request body parameters:\n{body}'))
def step_set_body_parameters(datatable, body, request):
    """
    The function that retrieves a table from the scenario and
    creates a body for the request to the API
    Args:
        datatable (datatable): kind of class object to interact with datatables
        body (datatable): body datatable composed by keys and values
        request (request): request fixture object
    """
    datatable.body = parse_str_table(body)

    body_dict = TableParser.\
        parse_to_dict(keys=datatable.body.columns['key'],
                      values=datatable.body.columns['value'])

    request.config.cache.set('body', body_dict)

    LOGGER.info(f'BODY TABLE: {request.config.cache.get("body", None)}')


@then(parsers.parse('the response status code should be {status_code:d}'))
def step_verify_response_code(status_code, request):
    """verify response code

    Args:
        status_code (str): status code
        request (str): request fixture object
    """
    expected_status_code = request.config.cache.get('status_code', None)
    assert_that(status_code).is_equal_to(expected_status_code)


@then(parsers.parse('the response body should be verified with:\n{table}'))
def step_verify_response_payload(table, request):
    """
    The function that verify that an inserted table is a subset of the
    response of the request
    Args:
        table (datatable): Table to compare with the response
        request (str): request fixture object
        """
    response = request.config.cache.get('response', None)

    datatable = parse_str_table(table)

    body_dict = TableParser. \
        parse_to_dict(keys=datatable.columns['key'],
                      values=datatable.columns['value'])

    assert_that(body_dict.items() <= response.items()).is_equal_to(True)


@then(parsers.parse(
    'the response schema should be verified with "{json_template}"'))
def step_verify_response_schema(json_template, request):
    """verify response schema

    Args:
        json_template(datatable): json to compare the schema
        request (str): request fixture object
    """
    response = request.config.cache.get('response', None)
    json_schema = read_json(f'./main/pivotal/resources/{json_template}')
    validate(response, json_schema)
    LOGGER.info('schema validation')
