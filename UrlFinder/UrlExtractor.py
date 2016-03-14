__author__ = 'rubico'

from HTMLParser import HTMLParser
from Models.Url import Url
import re


class UrlExtractor(HTMLParser):
    
    ANCHOR_TAG = 'a'
    HREF_ATTR = 'href'
    ATTR_NAME = 0
    ATTR_VALUE = 1
    
    urls = []
    page = None
    
    def handle_starttag(self, tag, attrs):
        if tag == UrlExtractor.ANCHOR_TAG:
            for attr in attrs:
                if attr[UrlExtractor.ATTR_NAME] == UrlExtractor.HREF_ATTR:
                    url = Url(UrlExtractor.__normalize_url(attr[UrlExtractor.ATTR_VALUE]), self.page.url.url)
                    self.urls.append(url)
                    
    def feed(self, page):
        self.urls = [] #Cleaning old urls
        self.page = page
        try:
            html = str(page.html).decode('utf-8')
        except:
            html = str(page.html)
        HTMLParser.feed(self, html)

    def __normalize_url(url):
        regex = '#.*'
        r = re.compile(regex)
        url = r.sub('', url) #remove anchor
        regex = '\?.*'
        r = re.compile(regex)
        url = r.sub('', url) #remove parameters
        return url