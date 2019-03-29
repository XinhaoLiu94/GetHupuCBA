# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HupuCBA(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    post_date = scrapy.Field()
    max_praise_nums = scrapy.Field()
    reply_nums = scrapy.Field()