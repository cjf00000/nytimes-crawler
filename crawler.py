from nytimesarticle import articleAPI
from mongo import *
from webparser import parse_article
import time

api = articleAPI('bd91258eb70d43f6bb104f5cade82f69')


def fetch_article(article):
    lead_paragraph = article["lead_paragraph"]
    headlines = article["headline"]["main"]
    url = article["web_url"]
    text, tokens = parse_article(url)

    doc = {
        'lead_paragraph': lead_paragraph,
        'headlines': headlines,
        'url': url,
        'text': text,
        'tokens': tokens,
        '_id': url
    }
    insert_doc(doc)
    return doc


def fetch_page(id):
    start = time.time()
    result = api.search(q='politics', begin_date=20160824, page=id)\
        ['response']['docs']

    total_num_tokens = 0
    for doc in result:
        d = fetch_article(doc)
        total_num_tokens += len(d['tokens'])

    elapsed = time.time() - start
    print('Page {} done in {} seconds, {} tokens.'
          .format(id, elapsed, total_num_tokens))


current_count = get_count()['count']
while current_count < 900:
    fetch_page(current_count)
    current_count += 1
    inc_count()
