__author__ = 'rubico'

from urlparse import urlparse
from enum import Enum


class UrlClasses(Enum):
    TRASH = 0
    FETCH = 1


class UrlClassifier:

    page = None
    page_domain = ''

    def __init__(self, page):
        self.page = page
        parsed_uri = urlparse(self.page.url.url)
        self.page_domain = parsed_uri.netloc

    def classify(self, url):
        parsed_uri = urlparse(url.url)
        if self.page_domain == parsed_uri.netloc:
            return UrlClasses.FETCH
        else:
            return UrlClasses.TRASH