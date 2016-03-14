__author__ = 'rubico'

from threading import Thread
from datetime import datetime
import urllib2
import time

from Models.Page import Page


class Fetcher(Thread):

    wait_time = 7
    dispatcher = None
    work = None
    
    def __init__(self, dispatcher, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.dispatcher = dispatcher
        self.wait_time = kwargs.get('wait_time', 7)
        
    def request_work(self):
        self.work = None
        if self.dispatcher.has_work():
            self.work = self.dispatcher.get_work()
            
    def do(self):
        if self.work is not None:
            self.fetch_url()

    def fetch_url(self):
        request = urllib2.Request(self.work.url)

        response = urllib2.urlopen(request)
        html = response.read()
        page = Page(self.work, html)
        page.save()
        print str(datetime.now()) +' '+ self.work.url
        
    def run(self):
        while True:
            self.request_work()
            if self.work:
                self.do()
                time.sleep(self.wait_time)