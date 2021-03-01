import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import IkbItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class IkbSpider(scrapy.Spider):
	name = 'ikb'
	start_urls = ['http://www.ikb.hr/hr/novosti']

	def parse(self, response):
		post_links = response.xpath('//div[@class="item"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Idi na sljedeću stranicu"]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = "Not stated"
		title = response.xpath('//h1[@class="page-header"]/text()').get()
		content = response.xpath('//div[@class="field-item even"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=IkbItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
