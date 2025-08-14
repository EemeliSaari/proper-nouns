import requests
from bs4 import BeautifulSoup

from .headers import from_env


def load_page(url: str) -> str:
    """load_page

    Loads raw content from a given url.

    Parameters
    ----------
    url: str
        Http url to a web page
    """
    res = requests.get(url, headers=from_env(), timeout=2, allow_redirects=False)
    res.raise_for_status()
    return res.text


def extract_text(content: str) -> str:
    """extract_text

    Parses typical html tags containing text such as paragraphs, lists
    and links.

    Parameters
    ----------
    content: str
        Raw content from the web page

    Returns
    -------
    text: str
        Parsed results
    """
    soup = BeautifulSoup(content, features='html.parser')
    text = ' '.join(x.text for x in soup.find_all(['p', 'li', 'a']))
    return text
