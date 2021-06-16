"""Module for constants"""
from enum import Enum

CONFIG_PATH = "main/pivotal/resources/config.json"
DEFAULT_FILE = "main/pivotal/resources/payload_projects.json"

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
