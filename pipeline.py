from index import Index
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals

class Pipeline:
    
    def __init__(self):
        # inverted index to store the content 
        self.index = Index()

        # get the settings for the crawler
        self.settings = get_project_settings()
        self.settings.set('ROBOTSTXT_OBEY', True) # obey robots.txt rules

        # initialize the crawler process
        self.process = CrawlerProcess(settings=self.settings)
        
        
    def start(self, spider, limit=5):
        """ Execute the crawler """
        dispatcher.connect(self._process_item, signal=signals.item_scraped) # use _process_item to process data from the spider
        self.process.crawl(crawler_or_spidercls=spider, limit=limit)
        self.process.start()
        
    
    def _process_item(self, item, spider):
        """ Process the item from the crawler """
        self.index.add(item['url'], item['content']) # add the content to the index