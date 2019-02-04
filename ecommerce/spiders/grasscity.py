# -*- coding: utf-8 -*-
from scrapy import Spider


class GrasscitySpider(Spider):
    name = 'grasscity'

    list_rules = {
        'css': {
            'price': '.add-to-cart-wrapper .old-price .price::text',
            'sales-price': '.add-to-cart-wrapper .special-price .price::text',
            'images': '.MagicToolboxSelectorsContainer a::attr(href)',
            'categories': '.breadcrumbs li a::text',
            'brand': '.block-attributes .data::text',
            'description': '.block-description .block-content',
        },
        'xpath': {
            'product_name': '//h1/text()',
        }
    }

    def __init__(self):
        self.url = "https://www.grasscity.eu/grasscity-the-weezy-jack-pod-smoking-pipe.html?___store=eu_en&nosto=new-products-home"
        self.start_urls = [self.url]

        self.domain = ["www.grasscity.eu"]
        self.allowed_domains = ["http://grasscity.eu/"]

    def parse(self, response):
        images = response.css(self.list_rules['css']['images']).extract()
        images = " , ".join(images)
        yield {
            'name': response.xpath(self.list_rules['xpath']['product_name']).extract_first(),
            'price': response.css(self.list_rules['css']['price']).extract_first(),
            'sales_price': response.css(self.list_rules['css']['sales-price']).extract_first(),
            'images': images,
            'description': response.css(self.list_rules['css']['description']).extract_first(),
            'categories': response.css(self.list_rules['css']['categories']).extract_first(),
            'brand': response.css(self.list_rules['css']['brand']).extract_first(),
        }






