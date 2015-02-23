# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserHistoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date_scraped = scrapy.Field()
    
    id = scrapy.Field()
    text = scrapy.Field()
    language = scrapy.Field()
    url = scrapy.Field()
    media = scrapy.Field()
    
    user_handle = scrapy.Field()
    user_display_name = scrapy.Field()
    user_id = scrapy.Field()
    user_profile_url = scrapy.Field()
    
    retweets = scrapy.Field()
    favorites = scrapy.Field()
    created_at= scrapy.Field()
