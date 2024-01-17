import scrapy
from scrapy.crawler import CrawlerProcess
import sqlite3

class DesignsByJuJuSpider(scrapy.Spider):
    name = 'designs'
    start_urls = ['https://www.designsbyjuju.com/all-designs']

    def __init__(self):
        super().__init__()
        # Connect to the SQLite database (replace 'your_database.db' with your database file)
        self.conn = sqlite3.connect('central_database.db')
        self.cursor = self.conn.cursor()

    def parse(self, response):
        # Extract information from each product item
        for product in response.css('div.item-content'):
            item = {
                'name': product.css('div.item-details strong.item-name a span.name::text').get(),
                'sku': product.css('div.item-details strong.item-name a span.sku::text').get(),
                'regular_price': product.css('div.price-box span.old-price span.price::text').get(),
                'special_price': product.css('div.price-box span.special-price span.price::text').get(),
                'product_link': product.css('div.item-details strong.item-name a::attr(href)').get(),
                'image_url': product.css('img.product-image-photo::attr(src)').get()
            }
            
            self.insert_into_database(item)

        # Follow the pagination link to the next page if it exists
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            # If there is no next page, close the database connection after processing all items
            self.conn.close()

    def insert_into_database(self, item):
        cursor.execute('''
            INSERT INTO items (company, set_title, item_title, image_url, price, set_price, item_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            "Designs By JuJu",
            item['sku'],
            item['name'],
            item['image_url'],
            item['special_price'],
            item['regular_price'],
            item['product_link']
        ))

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })

    process.crawl(DesignsByJuJu)
    process.start()
