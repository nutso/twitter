# -*- coding: utf-8 -*-
import scrapy
# import xml.etree
# from scrapy.contrib.spiders import CrawlSpider
from user_history.items import UserHistoryItem
from datetime import datetime
from bs4 import BeautifulSoup


class UserHistorySpiderSpider(scrapy.Spider):
    name = "user_history_spider"
    allowed_domains = ["twitter.com"]
    start_urls = (
        'https://mobile.twitter.com/BarackObama/',
    )

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
       
    # parse a single tweet detail page
    def parse_tweet(self, response):
        item = UserHistoryItem()
        
        item['date_scraped'] = datetime.now()
        item['url'] = response.url
        
        # TODO check for retweet .. different structure

        primary_tweet = response.css(".permalink-tweet-container")

        # Core Tweet Info
        item['id'] = primary_tweet.css("div.tweet::attr(data-tweet-id)").extract()[0]
        item['text'] = self.strip_html(primary_tweet.css("p.tweet-text").extract()[0]) # strip HTML
        item['language'] = primary_tweet.css("p.tweet-text::attr(lang)").extract()[0]
        item['created_at'] = primary_tweet.css(".js-short-timestamp::attr(data-time)").extract()[0]  # self.strip_html(primary_tweet.css("span.metadata span").extract()[0]) # TODO convert to date/time
        # TODO media (photos, urls, hashtags)

        # User Info
        item['user_handle'] = primary_tweet.css("div.tweet::attr(data-screen-name)").extract()[0]
        item['user_display_name'] = primary_tweet.css("div.tweet::attr(data-name)").extract()[0]
        item['user_id'] = primary_tweet.css("div.tweet::attr(data-user-id)").extract()[0]
        item['user_profile_url'] = primary_tweet.css(".permalink-header img.avatar::attr(src)").extract()[0]
        
        # Stats
        # TODO error handling when no retweets, etc.
        item['retweets'] = primary_tweet.css("li.js-stat-retweets a::attr(data-tweet-stat-count)").extract()[0]
        item['favorites'] = primary_tweet.css("li.js-stat-favorites a::attr(data-tweet-stat-count)").extract()[0]
        
        return item