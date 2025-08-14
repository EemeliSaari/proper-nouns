import os
import sys

import pytest
import requests
from fastapi.testclient import TestClient

root, _ = os.path.split(__file__)
sys.path.append(os.path.join(root, 'app'))

from app.api import app


@pytest.fixture(scope='session')
def test_client(request):
    yield TestClient(app)


@pytest.fixture(scope='session')
def test_url(request):
    yield 'https://httpbin.org/html'


@pytest.fixture(scope='session')
def test_html(test_url):
    res = requests.get(test_url)
    yield res.text
