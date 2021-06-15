"""
This module contains shared fixtures, steps, and hooks.
"""
import pytest

from main.core.utils.logger import CustomLogger
from main.core.utils.file_reader import read_json
from main.core.request_controller import RequestController

LOGGER = CustomLogger('test_logger')
REQUEST_CONTROLLER = RequestController()

CACHE_TAGS = ['body', 'response', 'status_code']

GLOBAL_CONTEXT = None
SCENARIO_TAGS = None

ENDPOINT_DEPENDENCIES = {
    "projects": None,
    "stories": "projects",
    "epic": "projects",
    "releases": "projects",
    "iteration": "projects",
    "tasks": ["projects", "stories"],
    "transitions": ["projects", "stories"],
    "reviews": ["projects", "stories"]
}

ENDPOINT_IDENTIFIERS = {
    "projects": "project_id",
    "stories": "story_id",
    "epic": "epic_id",
    "releases": "release_id",
    "iteration": "iteration_id",
    "tasks": "task_id",
    "transitions": "transition_id",
    "reviews": "review_id"
}


def build_endpoint(current_endpoint):
    """
    Parameters
    ----------
    current_endpoint (str): final endpoint for the request

    Returns
    -------

    built_endpoint (str): complete endpoint route
    """
    built_endpoint = ''
    dependencies = []
    for point, dependency in ENDPOINT_DEPENDENCIES:
        if point == current_endpoint:
            if isinstance(dependency, str):
                dependencies.append(dependency)
                built_endpoint += f'/{dependency}/<{dependency}_id>'
            elif isinstance(dependency, list):
                dependencies = dependency

    return built_endpoint


@pytest.fixture(autouse=True, scope='module')
def setup(request):
    """
    context of before all
    :return:
    """
    request.config.cache.get('endpoint', None)
    LOGGER.info("=============EXECUTED BEFORE ALL")

    def pytest_bdd_after_all():
        LOGGER.info("=============EXECUTED AFTER ALL")
        for cache_tag in CACHE_TAGS:
            LOGGER.info(f"cache tag: {cache_tag}")
            LOGGER.info(f"value: {request.config.cache.get(cache_tag, None)}")

    request.addfinalizer(pytest_bdd_after_all)


def pytest_bdd_before_scenario(request, scenario):
    """ pytest bdd before scenario

    Args:
        request (object): request object of fixture
        feature (object): feature object of pytest bdd
        scenario (object): scenario object of pytest bdd
    """
    LOGGER.info(f"=============STARTED SCENARIO {scenario.name}")
    for tag in scenario.tags:
        if "create" in tag:
            endpoint = f"/{tag.split('_')[-1]}"
            endpoint_id = ENDPOINT_IDENTIFIERS[endpoint[1:]]
            LOGGER.info(f"PRE-CONDITION: Create {endpoint}")

            payload_dict = read_json(
                f'./main/pivotal/resources/payload_{endpoint[1:]}.json')

            _, response = REQUEST_CONTROLLER.send_request(
                request_method='POST',
                endpoint=endpoint,
                payload=payload_dict)
            request.config.cache.set(f'{endpoint_id}', response['id'])
            LOGGER.info(f"NEW CACHE ENTRY: {endpoint_id} - {response['id']}")
            if f'{endpoint_id}' not in CACHE_TAGS:
                CACHE_TAGS.append(f'{endpoint_id}')


def pytest_bdd_step_error(step):
    """ pytest bdd step error

    Args:
        multiple args related with pytest bdd
    """
    LOGGER.debug(f'=============FAILED STEP: {step}')


def pytest_bdd_after_scenario(request, scenario):
    """ pytest bdd after scenario

    Args:
        request (object): request object of fixture
        feature (object): feature object of pytest bdd
        scenario (object): scenario object of pytest bdd
    """
    LOGGER.info(
        f"=============FINISHED SCENARIO {scenario.name} WITH STATUS: "
        f"{'FAILED' if scenario.failed else 'SUCCESS'}")

    for tag in scenario.tags:
        if "delete" in tag:
            element_id = request.config.cache.get('project_id', None)
            REQUEST_CONTROLLER.send_request(request_method='DELETE',
                                            endpoint=f"/{tag.split('_')[-1]}/"
                                                     f"{element_id}")

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
        :return:
        """
        return self.__str__()
