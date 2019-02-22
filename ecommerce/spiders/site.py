# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
import json
import pkgutil
import re


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
        data = {}
        # URL
        data['url'] = response.url

        # Name
        if self.json_config['fields']['name'] is not '':
            data['name'] = self.get_complete_text(response.xpath(self.json_config['fields']['name']))

        # price
        if self.json_config['fields']['price'] is not '':
            data['price'] = self.get_complete_text(response.xpath(self.json_config['fields']['price']))

        # Price Old
        if self.json_config['fields']['price_old'] is not '':
            data['price_old'] = self.get_complete_text(response.xpath(self.json_config['fields']['price_old']))

        # Availability
        if self.json_config['fields']['availability'] is not '':
            data['availability'] = self.get_complete_text(response.xpath(self.json_config['fields']['availability']))

        # Description
        if self.json_config['fields']['description'] is not '':
         data['description'] = self.get_complete_text(response.xpath(self.json_config['fields']['description']))

        # Rating
        if self.json_config['fields']['ratings'] is not '':
            data['ratings'] = self.get_complete_text(response.xpath(self.json_config['fields']['ratings']))

        # Categories
        if self.json_config['fields']['category'] is not '':
            data['category'] = response.xpath(self.json_config['fields']['category']).extract_first()

        # Images
        if self.json_config['fields']['image'] is not '':
            images = response.xpath(self.json_config['fields']['image']).extract()
            data['images'] = " , ".join(images)

        yield data

    def get_complete_text(self, html):
        text_list = []
        for element in html:
            item = element.extract()
            text = "".join(item)
            text_list.append(text)

        text = ''.join(text_list).strip(' \t\n\r')
        text = self.remove_quotations(text)
        text = self.replace_newline_char(text)
        text = self.strip_field(text)

        return text

    def remove_quotations(self, field):
        return field.replace(u"\u201d", "").replace(u"\u201c", "")

    def replace_newline_char(self, field):
        return field.replace(u"\n", " ").replace(u"\r", " ")

    def strip_field(self, field):
        return field.strip()

    def extract_digits(self, field):
        reference_regex = re.compile("\\d+")
        return reference_regex.findall(field)


