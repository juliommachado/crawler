import sqlite3

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
        self.start()
        
    def request_work(self):
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
            html = buffer(response.read())
            page = Page(self.work, html)
            page.save()
            print str(datetime.now())+': '+self.work.url
        except urllib2.URLError:
            self.dispatcher.fill_pool([self.work,])
            print '\n'+str(datetime.now())+': '+self.work.url+'\n'
        except sqlite3.OperationalError:
            self.dispatcher.fill_pool([self.work,])
            print '\n'+str(datetime.now())+': Database in lock - '+self.work.url+'\n'
        except:
            self.dispatcher.fill_pool([self.work,])
            print '\n'+str(datetime.now())+': '+self.work.url+'\n'

    def run(self):
        while True:
            self.request_work()
            if self.work:
                self.do()
                time.sleep(self.wait_time)