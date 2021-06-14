"""
This module contains shared fixtures, steps, and hooks.
"""
import pytest

from main.core.utils.logger import CustomLogger
from main.core.utils.file_reader import read_json
from main.core.request_controller import RequestController
from main.pivotal.utils.api_constants import HttpMethods as Methods

LOGGER = CustomLogger('test_logger')

CACHE_TAGS = ['body', 'id', 'response', 'status_code']

GLOBAL_CONTEXT = None
SCENARIO_TAGS = None


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
    for tag in scenario.tags:
        if "create" in tag:
            LOGGER.info("BEFORE SCENARIO: "
                        f"{request.config.cache.get('endpoint', None)}")
            endpoint = f"/{tag.split('_')[-1]}"

            payload_dict = read_json(
                f'./main/pivotal/resources/payload_{endpoint[1:]}.json')

            _, response = RequestController.get_instance().send_request(
                request_method=Methods.POST.value,
                endpoint=endpoint,
                payload=payload_dict)
            request.config.cache.set(f'{endpoint[1:]}_id',
                                     response.json()['id'])
            CACHE_TAGS.append(f'{endpoint[1:]}_id')


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
            element_id = request.config.cache.get('response', None)['id']
            RequestController.get_instance().\
                send_request(request_method=Methods.DELETE.value,
                             endpoint=f"/{tag.split('_')[-1]}/{element_id}")

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
