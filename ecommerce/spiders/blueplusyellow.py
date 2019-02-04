# -*- coding: utf-8 -*-
import scrapy


class BlueplusyellowSpider(scrapy.Spider):
    name = 'blueplusyellow'

    list_rules = {
        'css': {
            'price': '.product_infos .woocommerce-Price-amount::text',
            'sales-price': '.product_infos .woocommerce-Price-amount::text',
            'images': '.swiper-wrapper img::attr(src)',
            'categories': '.woocommerce-breadcrumb a::text',
            'rating': '.star-rating .rating::text',
            'description': '.wpb_wrapper',
        },
        'xpath': {
            'product_name': '//h1/text()',
        }
    }

    def __init__(self):
        self.url = "https://blueplusyellow.ca/product/bc-big-bud-hybrid/"
        self.start_urls = [self.url]

        self.domain = ["www.blueplusyellow.ca"]
        self.allowed_domains = ["http://blueplusyellow.ca/"]

    def parse(self, response):
        # Images
        images = response.css(self.list_rules['css']['images']).extract()
        images = " , ".join(images)
        # Price
        price = response.css(self.list_rules['css']['price']).extract()
        price = " - ".join(price)
        # Category
        categories =response.css(self.list_rules['css']['categories']).extract()
        categories = " - ".join(categories)
        yield {
            'name': response.xpath(self.list_rules['xpath']['product_name']).extract_first(),
            'price': price,
            'sales_price': price,
            'images': images,
            'description': response.css(self.list_rules['css']['description']).extract_first(),
            'categories': categories,
            'rating': response.css(self.list_rules['css']['rating']).extract_first(),
        }
