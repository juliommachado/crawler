from Dispatcher import Dispatcher
from Fetcher import Fetcher
from UrlFinder.UrlFinder import UrlFinder
import time

__author__ = 'rubico'

"""
dispatcher = Dispatcher()

fetcher1 = Fetcher(dispatcher)
fetcher2 = Fetcher(dispatcher)
fetcher3 = Fetcher(dispatcher)
fetcher4 = Fetcher(dispatcher)

url_finder = UrlFinder(dispatcher)
"""

import urllib2
import os

request = urllib2.Request('http://filepi.com/i/mqjSTFf')
request.add_header('Referer', 'http://it-ebooks.info/book/249/')
response = urllib2.urlopen(request)

content = response.read()

filepath = '/media/rubico/DADOS/crawler/storage/it-books/teste.pdf'
file = open(filepath, 'ab+')
file.write(content)
file.close()

serversize = 51915007
filesize = os.stat(filepath).st_size

response.close()

print 'Server size: '+str(serversize)
print 'File size: '+str(filesize)

print serversize == filesize


#continuar
request = urllib2.Request('http://filepi.com/i/mqjSTFf')
request.add_header('Referer', 'http://it-ebooks.info/book/249/')
request.add_header('Range', 'bytes=%d-' % (filesize,))
response = urllib2.urlopen(request)

content = response.read()

filepath = '/media/rubico/DADOS/crawler/storage/it-books/teste.pdf'
file = open(filepath, 'ab+')
file.write(content)
file.close()

serversize = 51915007
filesize = os.stat(filepath).st_size

response.close()

print 'Server size: '+str(serversize)
print 'File size: '+str(filesize)

print serversize == filesize