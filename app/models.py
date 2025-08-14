from pydantic.dataclasses import dataclass
from pydantic import HttpUrl


@dataclass
class UrlRequest:
    url: HttpUrl


@dataclass
class ParserResponse:
    values: dict[str, int]
