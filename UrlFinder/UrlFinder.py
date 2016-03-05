__author__ = 'rubico'

from threading import Thread
from Models.Page import Page
from UrlClassifier import UrlClassifier, UrlClasses
from UrlExtractor import UrlExtractor
from Database.Connection import Connection
import Settings


class UrlFinder(Thread):

    dispatcher = None
    connection = None
    url_extractor = None
    page = None
    
    def __init__(self, dispatcher, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.connection = Connection(Settings.sqllite_file_location)
        self.dispatcher = dispatcher
        self.url_extractor = UrlExtractor()
        self.start()
        
    def look_for_page(self):
        result = self.connection.execute('SELECT id, url_id, html, is_parsed FROM Page WHERE is_parsed = 1 LIMIT 1')

        self.page = None
        if result is not None:
            self.page = Page(tuple=result[0])

    def run(self):
        while True:
            self.look_for_page()
            if self.page is not None:
                self.url_extractor.feed(self.page)
                urls = self.url_extractor.urls

                #Classify all the urls
                url_classifier = UrlClassifier(self.page)
                for url in urls:
                    if url_classifier.classify(url) == UrlClasses.TRASH:
                        urls.remove(url)
                    elif url_classifier.classify(url) == UrlClasses.FETCH and url.fetch_id() is not None:
                        urls.remove(url)
                    url.save()

                self.page.mark_as_parsed()
                self.dispatcher.fill_pool(urls)