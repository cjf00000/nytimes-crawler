from mongo import *

docs = get_docs()
for doc in docs:
    print('dummy dummy ' + ' '.join(doc['tokens']))
