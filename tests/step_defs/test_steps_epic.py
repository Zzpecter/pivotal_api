"""
This module contains step definitions for boards_api.feature.
It uses the requests package:
http://docs.python-requests.org/
"""
import re
from assertpy import assert_that
from pytest_bdd import scenarios, given, when, then, parsers
from sttable import parse_str_table
from main.core.utils.logger import CustomLogger
from main.core.utils.table_parser import TableParser as Table_parser
from main.core.request_controller import RequestController
from main.core.utils.regex import RegularExpressionHandler as Regex

LOGGER = CustomLogger(name='api-logger')
my_request_controller = RequestController()

scenarios('../features/pivotal_epic_api.feature')


@given(parsers.parse('the following body parameters:\n{body}'))
def step_set_body_parameters(datatable, body, request):
    """set body parameters

    Args:
        datatable (datatable): kind of class object to interact with datatables
        body (datatable): body datatable composed by keys and values
        request (request): request fixture object
    """
    datatable.body = parse_str_table(body)

    body_dict = Table_parser. \
        parse_to_dict(keys=datatable.body.columns['key'],
                      values=datatable.body.columns['value'])

    request.config.cache.set('body', body_dict)
    LOGGER.info(f'BODY TABLE: {request.config.cache.get("body", None)}')


@given(parsers.parse('the "{http_method}" request to "{endpoint}" is sent'))
@when(parsers.parse('the "{http_method}" request to "{endpoint}" is sent'))
def step_send_request(http_method, endpoint, request):
    """[summary]

    Args:
        http_method (string): http method or verb
        endpoint (string): endpoint used to interact with request manager
        request (request): request fixture object
    """

    endpoint_name = re.findall(r"<(\w+)>", endpoint)
    body = request.config.cache.get('body', None)

    for replace_item in endpoint_name:
        tag_value = str(request.config.cache.get(replace_item, None))
        endpoint = Regex.replace_tag(f'<{replace_item}>',
                                     endpoint, tag_value)
    status_code, response = my_request_controller.send_request(http_method,
                                                               endpoint,
                                                               body)
    request.config.cache.set('response', response)
    request.config.cache.set('status_code', str(status_code))


@then(parsers.parse('the response status code should be {status_code}'))
def step_verify_response_code(status_code, request):
    """verify response code

    Args:
        status_code (string): status code
        request (string): request fixture object
    """
    expected_status_code = request.config.cache.get('status_code', None)
    assert_that(status_code).is_equal_to(expected_status_code)


@then(parsers.parse('the response body should be verified with:\n{table}'))
def step_verify_response_payload(table):  # pylint: disable=W0613
    """verify response payload

    Args:
        table (datatable)
    """
    LOGGER.info('Not implemented yet')


@then(parsers.parse('the response schema should be verified with "{json}"'))
def step_verify_response_schema(json):  # pylint: disable=W0613
    """verify response schema

    Args:
        json_template (datatable)
    """
    LOGGER.info('Not implemented yet')
