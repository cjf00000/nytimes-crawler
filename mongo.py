from pymongo import MongoClient
client = MongoClient()

db = client.nytimes
articles = db.articles
progress = db.progress


def insert_doc(doc):
    try:
        articles.insert_one(doc)
    except Exception:
        print('Duplicated entry')


def get_docs():
    doc_list = []
    for doc in articles.find():
        doc_list.append(doc)
    return doc_list


def drop_docs():
    articles.drop()


def inc_count():
    count = get_count()
    progress.update_one({'_id': count['_id']}, {'$inc': {'count': 1}})


def reset_count():
    count = get_count()
    progress.update_one({'_id': count['_id']}, {'$set': {'count': 0}})


def get_count():
    return progress.find_one()


def insert_count():
    progress.insert_one({'count': 0})


def delete_count():
    count = get_count()
    progress.delete_one({'_id': count['_id']})
