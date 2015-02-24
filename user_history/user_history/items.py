# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserHistoryItem(scrapy.Item):
    date_scraped = scrapy.Field()
    url = scrapy.Field()
    
    id_str = scrapy.Field()
    text = scrapy.Field()
    lang = scrapy.Field()
    entities = scrapy.Field()
    retweeted_status = scrapy.Field() # UserHistoryItem as well
    
    user = scrapy.Field()
    
    retweet_count = scrapy.Field()
    favorite_count = scrapy.Field()
    created_at= scrapy.Field()
    created_at_ts = scrapy.Field()
