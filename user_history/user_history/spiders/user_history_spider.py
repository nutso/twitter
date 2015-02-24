# -*- coding: utf-8 -*-
import scrapy
# import xml.etree
# from scrapy.contrib.spiders import CrawlSpider
from user_history.items import UserHistoryItem
from datetime import datetime
from bs4 import BeautifulSoup

# scrapy crawl user_history_spider -o scraped_data.json -a handle=BarackObama

class UserHistorySpiderSpider(scrapy.Spider):
    name = "user_history_spider"
    allowed_domains = ["twitter.com"]
    
    def __init__(self, *args, **kwargs):
        super(UserHistorySpiderSpider, self).__init__(*args, **kwargs)
        self.username = kwargs.get('handle')
        self.start_urls = ["https://mobile.twitter.com/" + self.username]

    def parse(self, response):
        links = response.css("table.tweet::attr(href)").extract()
        for link in links:
            link = "https://twitter.com" + link
            link = link.split("?")[0] # strip the ?p=v suffix if present
            # link is now the direct link to the (non-mobile) tweet details page

            yield scrapy.Request(link, self.parse_tweet)
        
        # next page
        next_page_link = response.css("div.w-button-more a::attr(href)").extract()[0]
        next_page_link = "https://mobile.twitter.com" + next_page_link
        print next_page_link
        yield scrapy.Request(next_page_link, self.parse)

    def strip_html(self, text):
        return BeautifulSoup(text).getText()
    
    def ts_to_twitter_date(self, ts):
        return datetime.fromtimestamp(ts).strftime("%a %b %d %H:%M:%S +0000 %Y")
       
    # parse a single tweet detail page
    def parse_tweet(self, response):
        item = UserHistoryItem()
        
        item['date_scraped'] = datetime.now()
        item['url'] = response.url
        
        primary_tweet = response.css(".permalink-tweet-container")

        # Core Tweet Info
        item['id_str'] = primary_tweet.css("div.tweet::attr(data-tweet-id)").extract()[0]
        item['text'] = self.strip_html(primary_tweet.css("p.tweet-text").extract()[0]) # strip HTML
        item['lang'] = primary_tweet.css("p.tweet-text::attr(lang)").extract()[0]
        item['created_at_ts'] = int(primary_tweet.css(".js-short-timestamp::attr(data-time)").extract()[0]) # UTC timestamp
        item['created_at'] = self.ts_to_twitter_date(item['created_at_ts'])

        # TODO photos
        
        item['entities'] = {}
        item['entities']['hashtags'] = [] # TODO only create array if there is at least one item
        for h in primary_tweet.css("a.twitter-hashtag b"):
            item['entities']['hashtags'].append(self.strip_html(h.extract()))

        item['entities']['links'] = [] # TODO only create array if there is at least one item
        for l in primary_tweet.css("a.twitter-timeline-link::attr(data-expanded-url)"):
            item['entities']['links'].append(l.extract())

        # User Info
        item['user'] = {}
        item['user']['screen_name'] = primary_tweet.css("div.tweet::attr(data-screen-name)").extract()[0]
        item['user']['name'] = primary_tweet.css("div.tweet::attr(data-name)").extract()[0]
        item['user']['id_str'] = primary_tweet.css("div.tweet::attr(data-user-id)").extract()[0]
        item['user']['profile_image_url'] = primary_tweet.css(".permalink-header img.avatar::attr(src)").extract()[0]
        
        # Stats
        retweets = primary_tweet.css("li.js-stat-retweets a::attr(data-tweet-stat-count)").extract()
        if retweets:
            item['retweet_count'] = retweets[0]
        else:
            item['retweet_count'] = 0
        
        favorites = primary_tweet.css("li.js-stat-favorites a::attr(data-tweet-stat-count)").extract()
        if favorites:
            item['favorite_count'] = favorites[0]
        else:
            item['favorite_count'] = 0
        
        # compare user_handle to self.username to determine if retweet
        # retweet-specific information is not apparently available via the site ... at least not without iterating over all the retweets
        if(item['user']['screen_name'] != self.username):
            # retweet
            retweet = UserHistoryItem()
            retweet['date_scraped'] = item['date_scraped']
            retweet['url'] = item['url']
            retweet['user'] = {}
            retweet['user']['screen_name'] = self.username
            retweet['retweeted_status'] = item
            return retweet
        else:
            return item