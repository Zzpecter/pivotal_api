"""
This module contains shared fixtures, steps, and hooks.
"""
import pytest

from main.core.utils.logger import CustomLogger
from main.core.utils.file_reader import read_json
from main.core.request_controller import RequestController
from main.pivotal.utils.api_constants import HttpMethods as http
from main.pivotal.utils.api_constants import ENDPOINT_IDENTIFIERS
from main.pivotal.utils.api_utils import build_endpoint, sort_tags_by_depth
from main.core.utils.string_utils import StringUtils as str_utils

from tests.utils.constants import CACHE_TAGS

LOGGER = CustomLogger('test_logger')


@pytest.fixture(autouse=True, scope='module')
def setup(request):
    """
    context of before all
    """
    request.config.cache.get('endpoint', None)
    LOGGER.info("=============EXECUTED BEFORE ALL")

    def pytest_bdd_after_all():
        LOGGER.info("=============EXECUTED AFTER ALL")
        RequestController.get_instance().close_session()
    request.addfinalizer(pytest_bdd_after_all)


def pytest_bdd_before_scenario(request, scenario):
    """ pytest bdd before scenario

    Args:
        request (object): request object of fixture
        scenario (object): scenario object of pytest bdd
    """
    LOGGER.info(f"=============STARTED SCENARIO {scenario.name}")
    LOGGER.debug(f"TAGS FOUND:  {scenario.tags}")

    scenario_tags = sort_tags_by_depth(scenario.tags)
    LOGGER.debug(f"SORTED TAGS:  {scenario_tags}")
    for tag in scenario_tags:
        LOGGER.info(f"PRE-CONDITION: TAG: {tag}")
        if "create" in tag:
            endpoint_name = f"{tag.split('_')[-1]}"
            endpoint = f"/{endpoint_name}"
            LOGGER.info(f"PRE-CONDITION: Create - raw: {endpoint}")
            built_endpoint = build_endpoint(endpoint_name)
            LOGGER.info(f"PRE-CONDITION: Create - built: {built_endpoint}")

            payload_dict = read_json(
                f'./main/pivotal/resources/payload_{endpoint[1:]}.json')

            tags_to_replace = str_utils.\
                search_text_between_tags(built_endpoint)

            LOGGER.debug(f'Tags found:  {tags_to_replace}')
            LOGGER.debug(f'un-processed endpoint:  {built_endpoint}')

            for txt in tags_to_replace:
                built_endpoint = str_utils.\
                    replace_string(built_endpoint,
                                   str(request.config.cache.get(txt, None)),
                                   f'<{txt}>')

                LOGGER.debug(f'WORKING on tags:  {built_endpoint}')

            LOGGER.info(f"PRE-CONDITION: Create - complete: {built_endpoint}")

            _, response = RequestController.get_instance().send_request(
                request_method=http.POST.value,
                endpoint=built_endpoint,
                payload=payload_dict)
            request.config.cache.set(f'{ENDPOINT_IDENTIFIERS[endpoint_name]}',
                                     response.json()['id'])
            CACHE_TAGS.append(f'{endpoint[1:]}_id')
            LOGGER.info(f"ADDED CACHE ENTRY: "
                        f"{ENDPOINT_IDENTIFIERS[endpoint[1:]]} -> "
                        f"{response.json()['id']}")


def pytest_bdd_step_error(step):
    """
    pytest bdd step error
    Args:
        step: multiple args related with pytest bdd

    Returns:

    """
    LOGGER.debug(f'=============FAILED STEP: {step}')


def pytest_bdd_after_scenario(request, scenario):
    """ pytest bdd after scenario

    Args:
        request (object): request object of fixture
        scenario (object): scenario object of pytest bdd
    """
    LOGGER.info(
        f"=============FINISHED SCENARIO {scenario.name} WITH STATUS: "
        f"{'FAILED' if scenario.failed else 'SUCCESS'}")

    for tag in scenario.tags:
        if "delete" in tag:
            # element_id = request.config.cache.get('project_id', None)

            element_id = request.config.cache.get('project_id', None)

            RequestController.get_instance().\
                send_request(request_method=http.DELETE.value,
                             endpoint=f"/projects/{element_id}")

    for tag in CACHE_TAGS:
        if request.config.cache.get(tag, None) is not None:
            request.config.cache.set(tag, None)


@pytest.fixture()
def datatable():
    """fixture to support implementation of datatables

    Returns:
        DataTable
    """
    return DataTable()


class DataTable:
    """
    Datatable Class to manage table elements
    """

    def __init__(self):
        pass

    def __str__(self):
        dt_str = ''
        for field, value in self.__dict__.items():
            dt_str = f'{dt_str}\n{field} = {value}'
        return dt_str

    def __repr__(self) -> str:
        """
        __repr__
        Returns:
             __str__ instance
        """
        return self.__str__()
