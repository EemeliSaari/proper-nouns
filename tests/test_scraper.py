import requests
import pytest

from app.scraper import load_page, extract_text


def test_invalid_url():
    invalid = 'https://absolotely-false.url'
    with pytest.raises(requests.exceptions.ConnectionError):
        _ = load_page(invalid)


def test_extract_text(test_html):
    res = extract_text(test_html)
    assert len(res) > 0


def test_extract_empty_text():
    res = extract_text('')
    assert res == ''


def test_invalid_html():
    invalid = """
        <!--  A SAMPLE set of slides  -->
        <slideshow title="Sample Slide Show" date="Date of publication" author="Yours Truly">
        <!-- TITLE SLIDE -->
            <slide type="all">
            <title>Wake up to WonderWidgets!</title>
            </slide>
        <!-- OVERVIEW -->
        </slideshow>
    """
    res = extract_text(invalid)
    assert res == ''
