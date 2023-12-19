import re

from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pep_parse.items import PepParseItem


class PepSpider(CrawlSpider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=['//section[@id="numerical-index"]'],
                allow=r'pep-\d+'
            ),
            callback='parse_pep',
            follow=False
        ),
    )

    def parse_pep(self, response):
        h1_text = response.xpath('//h1[@class="page-title"]/text()').get()
        h1_match = re.search(r'PEP (\d+).+– (.+)', h1_text)
        number, name = h1_match.group(1), h1_match.group(2)
        status = response.xpath(
            '//dl[@class="rfc2822 field-list simple"]//abbr/text()').get()
        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
