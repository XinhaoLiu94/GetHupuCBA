# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
import re
from hupu.items import HupuCBA
import datetime


class CbaSpider(scrapy.Spider):
    name = 'cba'
    allowed_domains = ['https://bbs.hupu.com/cba']
    start_urls = ['https://bbs.hupu.com/cba-1']

    def parse(self, response):

        post_urls = response.xpath("//a[@class='truetit']/@href").extract()
        for post_url in post_urls:
            print(post_url)
            yield Request(url = parse.urljoin(response.url,post_url), callback=self.parse_detail,dont_filter=True)

        url = response.url
        seperate = url.split('-')
        if len(seperate) == 1:
            url = "%s-%d" % (response.url.split('-')[0], 1)
        seperate = url.split('-')
        rank = int(seperate[1])
        if rank < 11:
            next_url = "%s-%d" % (response.url.split('-')[0], rank+1)
            yield Request(url=next_url, callback=self.parse, dont_filter=True)





    def parse_detail(self,response):
        hupuCba = HupuCBA()
        #Get the information on every page
        title = response.xpath("//h1[@id='j_data']/text()").extract()[0]
        author = response.xpath("//a[@class='u']/text()").extract()[0]
        post_date = response.xpath("//span[@class='stime']/text()").extract()[0]
        post_date = datetime.datetime.strptime(post_date, "%Y-%m-%d %H:%M").date()
        praise_array = response.xpath("//span[@class='ilike_icon_list']/span[@class='stime']/text()").extract()
        if praise_array == []:
            max_praise_nums = 0
        else:
            max_praise_nums = max(list(map(int, praise_array)))

        reply_nums = response.xpath("//span[@class='browse']/span[1]/text()").extract()[0]
        match_re = re.match("[0-9]+",reply_nums)
        if match_re:
            reply_nums = int(match_re.group(0))
        else:
            reply_nums = 0
        #print(reply_nums)
        hupuCba["title"] = title
        hupuCba["author"] = author
        hupuCba["post_date"] = post_date
        hupuCba["max_praise_nums"] = max_praise_nums
        hupuCba["reply_nums"] = reply_nums

        yield hupuCba

