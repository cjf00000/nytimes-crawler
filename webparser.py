from bs4 import BeautifulSoup
import urllib2
from nltk import word_tokenize
from nltk.corpus import stopwords
import re

url = "http://www.nytimes.com/2016/08/25/world/what-in-the-world/what-poor" \
      "-nations-need-to-get-by-money-from-migrants.html"


class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        # print "Cookie Manip Right Here"
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302


cookieprocessor = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
urllib2.install_opener(opener)
stop = set(stopwords.words('english'))


def parse_article(url):
    f = urllib2.urlopen(url)
    page = f.read().decode('utf8')
    f.close()

    soup = BeautifulSoup(page, 'html.parser')
    text_l = map(lambda x: x.get_text(),
                 soup.body.find_all('p', 'story-body-text'))

    text_str = ' '.join(text_l)
    text_str = text_str.replace('\u', '')
    text_str = re.sub('[^a-zA-Z\s\.\,\"\']', '', text_str)

    text_str_tokens = re.sub('[^a-zA-Z\s]', '', text_str).lower()

    tokenized_text_str = filter(lambda x: x not in stop,
                                word_tokenize(text_str_tokens))
    return text_str, tokenized_text_str
