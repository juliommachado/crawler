from Models.Page import Page

__author__ = 'rubico'

from threading import Thread
import urllib2
import time


class Fetcher(Thread):
    
    dispatcher = None
    work = None
    
    def __init__(self, dispatcher, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        #TODO (rubico) - see if the dispatcher is a istance of Dispatcher or any subclass
        self.dispatcher = dispatcher
        self.start()
        
    def get_work(self):
        self.work = None
        if self.dispatcher.has_work():
            self.work = self.dispatcher.get_work()
            
    def do(self):
        if self.work is not None:
            self.fetch_url()

    def fetch_url(self):
        request = urllib2.Request(self.work.url)
        try:
            response = urllib2.urlopen(request)
            html = response.read()
            page = Page(self.work, html)
            page.save()
            print self.work.url
        except: #If something went wrong, forget about it. On the next time it will try again: ;)
            print '\n ### '+self.work.url+'\n'
        
    def run(self):
        while True:
            self.get_work()
            if self.work:
                self.do()
                time.sleep(7)