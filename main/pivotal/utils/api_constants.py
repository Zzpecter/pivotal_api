"""Module for constants"""
from enum import Enum

CONFIG_PATH = "main/pivotal/resources/config.json"
DEFAULT_FILE = "main/pivotal/resources/payload_projects.json"


class HttpMethods(Enum):
    """Enum Created to manage Http Methods constants"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class Endpoints(Enum):
    """Enum Created to manage endpoint route constants"""
    PROJECTS = "projects/"
    STORIES = "stories/"
    EPIC = "epic/"
