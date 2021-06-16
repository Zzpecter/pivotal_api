"""Module for defining helper methods for the pivotal API"""
from api_constants import ENDPOINT_DEPENDENCIES


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
    for point, dependency in ENDPOINT_DEPENDENCIES.items():
        if point == current_endpoint:
            if isinstance(dependency, str):
                dependencies.append(dependency)
                built_endpoint += f'/{dependency}/<{dependency}_id>'
            elif isinstance(dependency, list):
                dependencies = dependency

    return built_endpoint