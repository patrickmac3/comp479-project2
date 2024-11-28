from index import Index
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals

class Pipeline:
    
    def __init__(self):
        
        self.index = Index()
        self.settings = get_project_settings()
        self.settings.set('ROBOTSTXT_OBEY', True)
        self.process = CrawlerProcess(settings=self.settings)
        
        
    def start(self, spider):
        dispatcher.connect(self._process_item, signal=signals.item_scraped)
        self.process.crawl(spider)
        self.process.start()
        
    
    def _process_item(self, item, spider):
        self.index.add(item['url'], item['content'])