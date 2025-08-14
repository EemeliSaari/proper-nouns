# Stage 1.
FROM python:3-slim-buster@sha256:d4354e51d606b0cf335fca22714bd599eef74ddc5778de31c64f1f73941008a4 as build

# Install the essentials
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	build-essential gcc 

# Install the app dependencies in the build stage
WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2.
FROM python:3-slim-buster@sha256:d4354e51d606b0cf335fca22714bd599eef74ddc5778de31c64f1f73941008a4

# Disabling the root user
RUN groupadd -g 999 scraper && \
    useradd -r -u 999 -g scraper scraper

RUN mkdir /usr/app && chown scraper:scraper /usr/app

WORKDIR /usr/app
COPY --chown=scraper:scraper --from=build /usr/app/venv ./venv
COPY --chown=scraper:scraper app/ /usr/app/

ENV PATH="/usr/app/venv/bin:$PATH"

# Download and install some of the basic spaCy models
RUN python -m spacy download en_core_web_sm

EXPOSE 8000
CMD [ "uvicorn", "api:app", "--host=0.0.0.0", "--port=8000" ]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f https://localhost:8000/healthcheck
