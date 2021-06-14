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
from main.core.utils.string_utils import StringUtils as Regex
from main.pivotal.utils.api_constants import HttpMethods as http
from main.core.request_controller import RequestController

LOGGER = CustomLogger('test_logger')


scenarios('../features/pivotal_projects.feature')


@given(parsers.parse('the "{http_method}" request to "{endpoint}" is sent'))
@when(parsers.parse('the "{http_method}" request to "{endpoint}" is sent'))
def step_send_request(http_method, endpoint, request):
    """[summary]

    Args:
        http_method (string): http method or verb
        endpoint (string): endpoint used to interact with request manager
        request (request): request fixture object
    """

    endpoint_name = endpoint.split('/')[1]

    new_id = request.config.cache.get(f"{endpoint_name}_id", None)
    body = request.config.cache.get('body', None)
    endpoint = Regex.replace_string(endpoint, str(new_id), '<id>')

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
    """set body parameters

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
        status_code (string): status code
        request (string): request fixture object
    """
    expected_status_code = request.config.cache.get('status_code', None)
    assert_that(status_code).is_equal_to(expected_status_code)


@then(parsers.parse('the response body should be verified with:\n{table}'))
def step_verify_response_payload(table, request):  # pylint: disable=W0613
    """verify response payload

    Args:
        table (datatable)
        request (string): request fixture object
    """
    response = request.config.cache.get('response', None)

    datatable = parse_str_table(table)

    body_dict = TableParser. \
        parse_to_dict(keys=datatable.columns['key'],
                      values=datatable.columns['value'])

    assert_that(body_dict.items() <= response.items()).is_equal_to(True)


@then(parsers.parse(
    'the response schema should be verified with "{json_template}"'))
def step_verify_response_schema(json_template, request):  # pylint:
    # disable=W0613
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
