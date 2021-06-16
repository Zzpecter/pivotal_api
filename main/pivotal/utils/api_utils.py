"""Module for defining helper methods for the pivotal API"""
from main.pivotal.utils.api_constants import ENDPOINT_DEPENDENCIES
from main.pivotal.utils.api_constants import ENDPOINT_IDENTIFIERS
from main.core.utils.logger import CustomLogger
LOGGER = CustomLogger('test_logger')


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
                                  f'<{ENDPOINT_IDENTIFIERS[dependency]}>' \
                                  f'/{point}/'
            elif isinstance(dependency, list):
                for dep in dependency:
                    built_endpoint += f'/{dep}/<{ENDPOINT_IDENTIFIERS[dep]}>'
                built_endpoint += f'/{point}/'
    return built_endpoint


def sort_tags_by_depth(tags):
    """
    Function for sorting tags, depending on the endpoint depth, calculated
    from the ENDPOINT_DEPENDENCIES constant.

     ...

     Parameters
    ----------
    tags (list): list of tags for the scenario

    Returns
    -------

    (list): sorted list of tags
    """
    LOGGER.debug(f"sort_tags_by_depth input:  {tags}")
    tag_level_dict = {}
    for tag in tags:
        tag_depth = 10
        if "create" in tag:
            tag_name = tag.split('_')[-1]
            dependencies = ENDPOINT_DEPENDENCIES[tag_name]
            if isinstance(dependencies, list):
                tag_depth = len(dependencies) + 1
            elif dependencies is None:
                tag_depth = 0
            else:
                tag_depth = 1
        tag_level_dict.update({tag: tag_depth})

    tag_level_dict = dict(sorted(tag_level_dict.items(),
                                 key=lambda item: item[1]))
    LOGGER.debug(f"sort_tags_by_depth output:  {tag_level_dict}")

    return tag_level_dict.keys()
