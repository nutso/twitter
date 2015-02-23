import scrapy

class ScrapyTweet(scrapy.Item):
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