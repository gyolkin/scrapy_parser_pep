import scrapy


class PepParseItem(scrapy.Item):
    Number = scrapy.Field()
    Name = scrapy.Field()
    Status = scrapy.Field()
