"""Module for defining helper methods for the pivotal API"""
from main.pivotal.utils.api_constants import ENDPOINT_DEPENDENCIES
from main.pivotal.utils.api_constants import ENDPOINT_IDENTIFIERS


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
    for point, dependency in ENDPOINT_DEPENDENCIES.items():
        if point == current_endpoint:
            if dependency is None:
                built_endpoint = '/projects'
            elif isinstance(dependency, str):
                built_endpoint += f'/{dependency}/' \
                                  f'<{ENDPOINT_IDENTIFIERS[dependency]}>'
            elif isinstance(dependency, list):
                for dep in dependency:
                    built_endpoint += f'/{dep}/<{ENDPOINT_IDENTIFIERS[dep]}>'
    return built_endpoint
