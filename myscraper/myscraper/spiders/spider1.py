import scrapy


class QuotesSpider(scrapy.Spider):
    name = "myspider"

    def start_requests(self):
        # urls to scrape data
        urls = [
            'https://damro.lk/product-category/living-room/sofa-and-lobby-chairs/sofa/',
            'https://damro.lk/product-category/bedroom/bedroom-furniture/beds/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Getting the Product Name, Description and Price of the products
        for product in response.css('section.product'):
            yield {
                'Product Name': product.css('h3.heading-title a::text').get(),
                'Description': product.css('span.price p::text').get(),
                'Price': product.css('p.cash-price::text').get()
            }

        # To get the data from paginated contents
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
