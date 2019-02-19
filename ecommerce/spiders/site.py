# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
import json
import pkgutil


class GrasscitySpider(scrapy.Spider):
    name = 'site'

    def __init__(self, config=None, *args, **kwargs):

        try:
            data = pkgutil.get_data('ecommerce',config)
            print("Data obtained from config: ", data)
            self.json_config = json.loads(data)
        except IOError as FileNotFoundException:
            raise CloseSpider(reason=FileNotFoundException)

        if self.json_config is not None:
            self.start_urls = self.json_config['start_urls']

            self.domain = self.json_config['domain']
            self.allowed_domains = self.json_config['allowed_domains']
        else:
            raise CloseSpider(reason="Json file is not valid. Closing spider...")

    def parse(self, response):

        # Process each URL
        urls = response.xpath(self.json_config['links']['detail']).extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            yield Request(absolute_url, cookies={'store_language':'en'}, callback=self.parse_site)

        # Process next pages
        next_page_url = response.xpath(self.json_config['links']['next_page']).extract()
        next_page_url = next_page_url[1] if len(next_page_url) > 1 else next_page_url[0]
        absolute_next_url = response.urljoin(next_page_url)
        yield Request(absolute_next_url)

    def parse_site(self, response):

        # URL
        url = response.url

        # Name
        name = self.get_complete_text(response.xpath(self.json_config['fields']['name']))

        # price
        price = self.get_complete_text(response.xpath(self.json_config['fields']['price']))

        # Price Old
        price_old = self.get_complete_text(response.xpath(self.json_config['fields']['price_old']))

        # Availability
        availability = self.get_complete_text(response.xpath(self.json_config['fields']['availability']))

        # Description
        description = self.get_complete_text(response.xpath(self.json_config['fields']['description']))

        # Rating
        rating = self.get_complete_text(response.xpath(self.json_config['fields']['rating']))

        # Categories
        categories = response.xpath(self.json_config['fields']['categories']).extract_first()

        # Images
        images = response.xpath(self.json_config['fields']['image']).extract()
        images = " , ".join(images)
        yield {
            'url': url,
            'name': name,
            'price': price,
            'sales_price': price_old,
            'images': images,
            'availability': availability,
            'description': description,
            'rating': rating,
            'categories': categories,
        }

    def get_complete_text(self, html):
        text_list = []
        for element in html:
            item = element.xpath('.//text()').extract()
            text = " ".join(item)
            text_list.append(text)

        return ''.join(text_list).strip(' \t\n\r')


