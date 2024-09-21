import scrapy
from bookscraping.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        book = response.css('article.product_pod')

        
        for book in book:
            relative_url = book.css('h3 a ::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url = "https://books.toscrape.com/" + relative_url 
            else:
                book_url = "https://books.toscrape.com/catalogue/" + relative_url

            yield response.follow( book_url, callback =self.parse_book_page)



            next_page = response.css('li.next a::attr(href)').get()


            if next_page:
                if 'catalogue/' in next_page:
                    next_page_url = "https://books.toscrape.com/" + next_page 
                else:
                    next_page_url = "https://books.toscrape.com/catalogue/" + next_page
        
                yield response.follow( next_page_url, callback = self.parse)



    def parse_book_page(self, response):
        
        table_rows = response.css('table tr')
        book_items = BookItem()
        
    
        book_items['url'] = response.url,
        book_items['title'] = response.css('.product_main h1::text').get(),
        book_items['product_type'] = table_rows[1].css("td ::text").get(),
        book_items['price_excl_tax'] = table_rows[2].css("td ::text").get(),
        book_items['price_incl_tax'] = table_rows[3].css("td ::text").get(),
        book_items['tax'] = table_rows[4].css("td ::text").get(),
        book_items['availablity'] = table_rows[5].css("td ::text").get(),
        book_items['num_reviews'] = table_rows[6].css("td ::text").get(),
        book_items['stars'] = response.css("p.star-rating").attrib['class'],
            #'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active]/preceding-sibling::li[1]/a/text()").get(),
        book_items['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_items['price'] = response.css('p.price_color ::text').get(),
        
        yield book_items