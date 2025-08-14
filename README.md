# Proper Noun Scraper

This toy project aims to provide a service to scrape proper nouns from a web page. The service is accessible with REST API.

---

## Structure

As the project is simple enough and there is no immediate use to use a standard [setup.py](https://packaging.python.org/en/latest/tutorials/packaging-projects/) structure.

```
.root
|
├── app
│   ├── api.py              # REST app
│   ├── models.py           # pydantic data models
│   ├── lang                # spaCy extension
│   └── scraper             # Web scraping module
|
├── conftest.py             # Pytest fixtures and plugins
├── tests                   # Unittests for modules and API
|
├── requirements.txt        # dependencies
|
├──.dockerignore
├── Dockerfile
|
└── README.md
```

---

## Configuration

The project has two parameters that can be configured to allow service to adjust to different languages.

- `MODEL_NAME`: [spaCy Model](https://spacy.io/usage/models) name or path to trained model
- `SERVICE_LANG`: [Accept-Language](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language) for web scraper headers.

> **NOTE:** The service does not check the web page content language and some of the sites just ignore the Accept-Language headers.

---

## Installation

This project uses some of the new Python features such as the new [type hinting](https://docs.python.org/3/whatsnew/3.9.html#type-hinting-generics-in-standard-collections) so version +3.9 is required.

### 3rd Party Requirements

- [spaCy](https://spacy.io/) High level API for various natural language processing tasks
- [FastAPI](https://fastapi.tiangolo.com/) High performance web framework for Python
- [Pytest](https://docs.pytest.org/en/6.2.x/) Python testing framework
- [Beautifulsoup4](https://beautiful-soup-4.readthedocs.io/en/latest/) Python library to handle html data
- [uvicorn](https://www.uvicorn.org/) ASGI server for FastAPI

### Local

To install dependencies to your local Python environment run

> ! Usage of [virtualenv](https://docs.python.org/3/tutorial/venv.html) or [conda](https://docs.conda.io/en/latest/) is recommended

```bash
(.env)$ pip install -r requirements.txt
(.env)$ python -m spacy download en_core_web_sm
```

To start the server for local development

```bash
(.env)$ cp app/
(.env)$ python -m uvicorn api:app --reload
```

To use a different [Language](https://spacy.io/usage/models#languages)

For example German:

```bash
# Install the model
(.env)$ python -m spacy download de_core_news_sm
# Configure model name as environment parameter
(.env)$ export MODEL_NAME=de_core_news_sm
```

### Docker

The docker image is based on the

```bash
docker build -t propn-scraper .
docker run -p 8000:8000 propn-scraper
```

To run and install different models for docker

```bash
docker run -e MODEL_NAME=de_core_news_sm -e SERVICE_LANG=ge -p 8000:8000 propn-scraper /bin/bash -c "python -m spacy download de_core_news_sm && python -m uvicorn api:app --host=0.0.0.0 --port=8000"
```

---

## Usage

After installation you should have the service up and running and accessable through port `8000`.

In this section I cover example uses using [curl](https://curl.se/). You can also navigate to the swagger page: http://localhost:8000/docs

### Basic

counting proper nouns

**Request**

```bash
curl --location \
    --request POST 'http://localhost:8000/pos/count_propn/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "url": "https://danluu.com/writing-non-advice/"
    }'
```

**Response**

```json
{
    "values": {
        "Patreon": 1,
        "Joel Spolsky": 2,
        "Paul Graham": 5,
        ...
    }
}
```

healthcheck

**Request**

```
curl --location --request GET 'http://localhost:8000/healthcheck'
```

**Response**

```json
{
  "status": "alive"
}
```

## Testing

The tests can be run locally

```bash
(.env)$ pytest -v .
```
