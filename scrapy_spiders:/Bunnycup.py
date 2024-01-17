import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sqlite3


class BunnyCupSetSpider(scrapy.Spider):
    name = 'bunnycup_set'
    start_urls = ['https://www.bunnycup.com/embroidery-designs-all']
    # Configure logging to suppress warnings
    custom_settings = {
        'LOG_LEVEL': 'ERROR',  # Set to 'ERROR' to only display error messages
        'LOG_ENABLED': True,    # Set to False to completely disable logging
    }

    rules = (
        Rule(LinkExtractor(allow=r'/embroidery-designs-all\?page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/embroidery-design-'), callback='parse_item'),
    )

    def __init__(self):
        self.items = []

        #database
        self.conn = sqlite3.connect('../central_database.db')
        self.cursor = self.conn.cursor()

    def parse(self, response):
        # Extract links to specific sets
        set_links = response.css('a[itemprop="url"]::attr(href)').getall()
        full_set_links = [response.urljoin(link) for link in set_links]
        
        # Follow links to specific sets
        for full_set_link in full_set_links:
            yield scrapy.Request(url=full_set_link, callback=self.parse_set)

    def parse_set(self, response):
        # Extract information from the set page
        set_title = self.extract_set_title_from_url(response.url)

        # Extract links to individual items within the set
        for product in response.css('a[itemprop="url"]'):
            product_link = product.css('::attr(href)').get()
            product_link = response.urljoin(product_link)           
            yield scrapy.Request(url=product_link, callback=self.parse_item)

    def parse_item(self, response):
        # Extract information from the individual item page
        title = response.css('h1[itemprop="name"]::text').get()
        image_url = response.css('img#ctl00_contentMain_imgDesign::attr(src)').get()
        set_price = response.css('span[itemprop="price"]::text').get()
        price = response.css('h2.text-center span[itemprop="price"]::text').get()
        set_title = self.extract_set_title_from_url(response.url)


        # Insert the item into the database
        self.cursor.execute('''
            INSERT INTO items (company, set_title, item_title, image_url, price, set_price, item_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ("Bunnycup", set_title, title, image_url, price, set_price, response.url))
        
        yield {
            'item_title': title,
            'image_url': image_url,
            'price': price,
            'set_price': set_price
        }

    def extract_set_title_from_url(self, url):
        patterns = [
            r'https://www\.bunnycup\.com/embroidery-design-([^/]+)/.*',
            r'https://www\.bunnycup\.com/embroidery-design-([^/]+)$',
            r'https://www\.bunnycup\.com/([^/]+)/embroidery-design-([^/]+)/.*'
        ]

        for pattern in patterns:
            match = re.match(pattern, url)
            if match:
                set_name = match.group(1)
                return set_name.replace('-', ' ')

        return None
    
    def closed(self, reason):
        # Commit changes to the database
        self.conn.commit()

        # Close the database connection
        self.conn.close()

        # Print a message indicating where the data is stored
        print("Final items written to the database.")
        
if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })

    process.crawl(BunnyCupSetSpider)
    process.start()
