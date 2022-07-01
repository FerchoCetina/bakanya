import pytest
import requests

from main import get_cats_facts, STATUS_HTTP


@pytest.mark.parametrize(
    "number, status",
    [
        ("abc", STATUS_HTTP.NON_CONTENT),
        ("0", STATUS_HTTP.NON_CONTENT),
        ("10", STATUS_HTTP.OK),
        ("200", STATUS_HTTP.OK),
        ("450", STATUS_HTTP.PARTIAL_CONTENT),
        ("501", STATUS_HTTP.OK),
    ]
)
def test_api(number, status):
    try:
        response_test = requests.get(F"http://127.0.0.1:5000/cat-facts/{number}")
        assert response_test.status_code == status
    except(requests.exceptions.ReadTimeout, requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        False