__author__ = 'rubico'

from HTMLParser import HTMLParser
from Models import Url


class UrlExtractor(HTMLParser):
    
    ANCHOR_TAG = 'a'
    URL_ATTR = 'href'
    ATTR_NAME = 0
    ATTR_VALUE = 1
    
    urls = []
    
    def handle_starttag(self, tag, attrs):
        if tag == UrlParser.ANCHOR_TAG:
            for attr in attrs:
                if attr[UrlParser.ATTR_NAME] == UrlParser.URL_ATTR:
                    self.urls.append(Url(attr[UrlParser.ATTR_VALUE]))
                    
    def feed(self, data):
        self.urls = [] #Cleaning old urls
        HTMLParser.feed(self, data)