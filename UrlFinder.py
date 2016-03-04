__author__ = 'rubico'

from threading import Thread
from UrlParser import UrlParser


class UrlFinder(Thread):
    
    connection = None
    url_parser = None
    
    
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.url_parser = UrlParser()
        pass #Let's pretend that the connection is working ;)
        self.start()
        
    def get_page(self):
        pass #goes to the database and gets only one page
        #return None in case of no page without parse.
 
    def run(self):
        while True:
            if page is not None:
                url_parser.feed(page)