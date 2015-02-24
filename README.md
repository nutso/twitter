Twitter ~ Playing with Python

Requirements:
* Python
* Scrapy
* BeautifulSoup4

Usage: change to the user_history directory and run:

scrapy crawl user_history_spider -s LOG_FILE=scrapy.log -s LOG_LEVEL='INFO' -o scraped_data.json -a handle=BarackObama 

(replace "BarackObama" with the Twitter user handle of interest)


Tweets are returned as best approximating the Twitter tweet format (ref: https://dev.twitter.com/overview/api/tweets) as possible.

Additional fields include:
* created_at_ts: UTC timestamp corresponding to the created_at field
* entities item contains pure array lists of the correpsonding entity, without additional information (i.e. tweet.entities.hashtags is an array of hashtag terms only)
* date_scraped: date and time when the record was scraped ("now")
* url: actual url from which the record was scraped