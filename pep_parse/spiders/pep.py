import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        peps = response.css("section#numerical-index td a::attr(href)")
        for pep_link in peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = re.search(
            r"PEP\s(?P<number>\d+)\W+(?P<name>.+)$",
            response.css("h1.page-title::text").get(),
        ).groups()
        status = response.css(
            'dt:contains("Status") + dd'
        ).css("abbr::text").get()
        data = {
            "number": number,
            "name": name,
            "status": status,
        }
        yield PepParseItem(data)
