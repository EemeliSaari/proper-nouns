import os


def default(lang: str) -> dict[str, str]:
    """Default headers for scraping"""
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
               'Accept-Language': lang, 'Accept': 'text/html', 'Refer': 'http://wwww.google.com'}
    return headers


def from_env() -> dict[str, str]:
    """Loads headers from environemnt"""
    lang = os.environ.get('SERVICE_LANG', 'en')
    return default(lang=lang)
