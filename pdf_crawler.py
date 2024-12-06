import io 
import PyPDF2
import scrapy 
import threading 
import re 

class PdfCrawler(scrapy.Spider):
    name = 'pdf_crawler'
    start_urls = ['https://spectrum.library.concordia.ca/']
    
    def __init__(self, limit=5, *args, **kwargs):
        super(PdfCrawler, self).__init__(*args, **kwargs)
    
        # limit the number of pdfs to be extracted 
        self.limit = int(limit)
        
        # counter to keep track of the number of pdfs extracted
        self.counter = 0
        self.counter_lock = threading.Lock() # lock to prevent it from being accessed by multiple threads at the same time
        
        
    def start_requests(self):
        """ Entry point of the crawler """
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_main_page)
            
    
    def parse_main_page(self, response):
        """ From the main page, find the link for browsing  """
        browse_link = response.css('#main_menu_browse a::attr(href)').get()
        if not browse_link:
            self.logger.error("Browse link not found on the main page.")
            return
        yield response.follow(browse_link, callback=self.parse_browse_page)
        
    def parse_browse_page(self, response):
        """ From the browse page, find the link document type """
        document_type_link = response.css("a[href*='/view/doctype/']::attr(href)").get()
        if not document_type_link:
            return
        yield response.follow(document_type_link, callback=self.parse_document_type_page)
        
    def parse_document_type_page(self, response):
        """ From the document type page, find the link for thesis """
        thesis_link = response.xpath('//div[@class="ep_view_menu"]//li[a[contains(text(), "Thesis")]]/a/@href').get()
        if not thesis_link:
            return
        yield response.follow(thesis_link, callback=self.parse_publication_year_page)
    
    def parse_publication_year_page(self, response):
        """ From the pick a year page, extract the link for each year """
        for i in range(1, 4):
            div_selector = f'div.ep_view_col_{i} ul li a::attr(href)'
            year_links = response.css(div_selector).getall()
            for year_link in year_links:
                if year_link and year_link.endswith('.html'):
                    
                    
                    """ 
                        Assuming the year link (href) has the following format -> 2010.html 
                        And that more recent years are more likely to have readable pdfs, 
                        we use the year to set the priority of the request
                    """
                    match = re.search(r'(\d{4})\.html$', year_link)
                    if match:
                        year = int(match.group(1))
                        priority = -year 
                        self.logger.info(f"Enqueueing {year_link} with priority {priority}")
                        yield response.follow(year_link, callback=self.parse_thesis_list_page, priority=priority)
             
    
    def parse_thesis_list_page(self, response):
        """ From the thesis list page, extract the link for individual thesis pages """
        page_links = response.css('div.ep_view_page.ep_view_page_view_doctype > p > a::attr(href)').getall()
        for page_link in page_links:
            yield response.follow(page_link, callback=self.parse_thesis_page)
            
    def parse_thesis_page(self, response):
        """ From the individual thesis page, extract the link for the pdf """
        if self.counter >= self.limit: 
            self.crawler.engine.close_spider(self, "PDF limit reached")
            return
        pdf = response.css('span.ep_document_citation a.ep_document_link::attr(href)').get()
        if pdf:
            yield response.follow(pdf, callback=self.parse_pdf) 
            
    
    def parse_pdf(self, response):
        """ Parse the pdf content """
        with self.counter_lock:
            if self.counter >= self.limit:
                self.crawler.engine.close_spider(self, "PDF limit reached")
                return
            self.counter += 1
            
        pdf_stream = io.BytesIO(response.body)
        
        try:
            reader = PyPDF2.PdfReader(pdf_stream)
            if not reader.pages:
                return 
        except Exception as e:
            self.logger.error(f"Error reading pdf: {response.url}")
            return 
        
        for page in reader.pages:
            if not (content:=page.extract_text()).strip():
                continue 
            yield {
                "url": response.url,
                "content": content
            }

        