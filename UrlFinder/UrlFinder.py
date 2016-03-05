from UrlClassifier import UrlClassifier, UrlClasses
from UrlExtractor import UrlExtractor

__author__ = 'rubico'

from threading import Thread


class UrlFinder(Thread):
    
    connection = None
    url_extractor = None
    page = None
    
    
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.url_extractor = UrlExtractor()
        pass #Let's pretend that the connection is working ;)
        self.start()
        
    def look_for_page(self):
        pass #goes to the database and gets only one page
        #return None in case of no page without parse.
 
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
