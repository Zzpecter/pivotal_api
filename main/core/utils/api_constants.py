"""Module for constants"""
from enum import Enum


class HttpMethods(Enum):
    """Enum Created to manage Http Methods constants"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
