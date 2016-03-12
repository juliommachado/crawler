from Dispatcher import Dispatcher
from Fetcher import Fetcher
from UrlFinder.UrlFinder import UrlFinder
import time

__author__ = 'rubico'


dispatcher = Dispatcher()

fetcher1 = Fetcher(dispatcher)
fetcher2 = Fetcher(dispatcher)
fetcher3 = Fetcher(dispatcher)
fetcher4 = Fetcher(dispatcher)

url_finder = UrlFinder(dispatcher)