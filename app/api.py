import os
from collections import Counter

import requests
import spacy
from fastapi import Body, FastAPI, HTTPException

import lang
from models import ParserResponse, UrlRequest
from scraper import extract_text, load_page


app = FastAPI(
    title='Propn Scraper',
    version='1.0',
    description='Web scraping for proper nouns'
)

model = os.environ.get('MODEL_NAME', 'en_core_web_sm')

nlp = spacy.load(model, disable=['lemmatizer', 'ner'])
nlp.add_pipe("joint_propn", last=True)


@app.post('/pos/count_propn', response_model=ParserResponse, tags=['propn'])
async def count_propn(body: UrlRequest = Body(..., example={'url': 'https://httpbin.org/html'})):
    try:
        html = load_page(url=body.url)
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=400, detail=f'Connection failed to {body.url}')

    text = extract_text(content=html)
    doc = nlp(text=text)

    return {'values': Counter(span.text for span in doc._.joint_propn)}


@app.get('/healthcheck', tags=['health'])
async def healthcheck():
    return {'status': 'alive'}
