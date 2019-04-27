import pytest
from pytest_httpserver import HTTPServer
import requests


def test_my_client(httpserver): 
    httpserver.expect_request("/trees").respond_with_json({"myFavouriteTree":"Oak"})
    assert requests.get(httpserver.url_for("/trees")).json() == {"myFavouriteTree":"Oak"}
