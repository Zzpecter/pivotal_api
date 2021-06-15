"""
This module contains step definitions for pivotal_projects.feature.
"""
from assertpy import assert_that
from pytest_bdd import scenarios, given, when, then, parsers
from sttable import parse_str_table
from jsonschema import validate

from main.core.utils.file_reader import read_json
from main.core.utils.logger import CustomLogger
from main.core.utils.table_parser import TableParser as table_parser
from main.core.utils.regex import RegularExpressionHandler as regex
from main.core.request_controller import RequestController

from tests.step_defs.conftest import ENDPOINT_IDENTIFIERS, \
    ENDPOINT_DEPENDENCIES

LOGGER = CustomLogger('test_logger')
REQUEST_CONTROLLER = RequestController()

scenarios('../features/pivotal_projects.feature')

ENDPOINT_NAME = "/projects"
ENDPOINT_ID = "project_id"


@given(parsers.parse('the "{http_method}" request to "{endpoint}" is sent'))
@when(parsers.parse('the "{http_method}" request to "{endpoint}" is sent'))
def step_send_request(http_method, endpoint, request):
    """[summary]

    Args:
        http_method (string): http method or verb
        endpoint (string): endpoint used to interact with request manager
        request (request): request fixture object
    """

    tags_to_replace = regex.search_text_between_tags(endpoint)

    LOGGER.debug(f'Tags found:  {tags_to_replace}')
    LOGGER.debug(f'un-processed endpoint:  {endpoint}')

    for tag in tags_to_replace:
        endpoint = regex.replace_tag(f'<{tag}>',
                                     endpoint,
                                     str(request.config.cache.get(tag, None)))
        LOGGER.debug(f'WORKING on tags:  {endpoint}')

    LOGGER.debug(f'processed endpoint:  {endpoint}')

    body = request.config.cache.get('body', None)

    status_code, response = REQUEST_CONTROLLER.send_request(
            request_method=http_method,
            endpoint=endpoint,
            payload=body)

    request.config.cache.set('status_code', status_code)
    request.config.cache.set('response', response)
    LOGGER.info(f"NEW CACHE ENTRY: status_code - {status_code}")
    LOGGER.info(f"NEW CACHE ENTRY: response - {response}")


@given(parsers.parse('the following request body parameters:\n{body}'))
def step_set_body_parameters(datatable, body, request):
    """set body parameters

    Args:
        datatable (datatable): kind of class object to interact with datatables
        body (datatable): body datatable composed by keys and values
        request (request): request fixture object
    """
    datatable.body = parse_str_table(body)

    body_dict = table_parser.\
        parse_to_dict(keys=datatable.body.columns['key'],
                      values=datatable.body.columns['value'])

    request.config.cache.set('body', body_dict)

    LOGGER.info(f'BODY TABLE: {request.config.cache.get("body", None)}')


@then(parsers.parse('the response status code should be {status_code:d}'))
def step_verify_response_code(status_code, request):
    """verify response code

    Args:
        status_code (string): status code
        request (string): request fixture object
    """
    expected_status_code = request.config.cache.get('status_code', None)
    assert_that(status_code).is_equal_to(expected_status_code)


@then(parsers.parse('the response body should be verified with:\n{table}'))
def step_verify_response_payload(table, request):
    """verify response payload

    Args:
        table (datatable)
        request (string): request fixture object
    """
    response = request.config.cache.get('response', None)

    datatable = parse_str_table(table)

    body_dict = table_parser. \
        parse_to_dict(keys=datatable.columns['key'],
                      values=datatable.columns['value'])

    assert_that(body_dict.items() <= response.items()).is_equal_to(True)


@then(parsers.parse(
    'the response schema should be verified with "{json_template}"'))
def step_verify_response_schema(json_template, request):
    """verify response schema

    Args:
        table (datatable)
        request (string): request fixture object
    """
    response = request.config.cache.get('response', None)
    json_schema = read_json(f'./main/pivotal/resources/{json_template}')
    validate(response, json_schema)  # if it fails it should raise error
    # (returns nothing)
    LOGGER.info('schema validation')
