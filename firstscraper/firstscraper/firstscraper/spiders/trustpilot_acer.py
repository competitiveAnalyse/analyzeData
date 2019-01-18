# -*- coding: utf-8 -*-
import scrapy

starturl = 'https://www.trustpilot.com'
user_links = []
nationalities = []

class TrustpilotMsiSpider(scrapy.Spider):
    name = 'trustpilot_acer'
    allowed_domains = ['trustpilot.com/review/www.acer.com?languages=en',
                       'trustpilot.com/review/acer.co.uk?languages=en',
                       'trustpilot.com/review/acer-laptops.co.uk?languages=en']
    start_urls = ['https://www.trustpilot.com/review/www.acer.com?languages=en',
                  'https://www.trustpilot.com/review/acer.co.uk?languages=en',
                  'https://www.trustpilot.com/review/acer-laptops.co.uk?languages=en']
    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'/home/juan/trustpilot_acer.json',
        'FEED_EXPORT_ENCODING':'utf-8',
        'CONCURRENT_REQUESTS':'8',
        'ROBOTSTXT_OBEY':'False'
    }
    
    def parse(self, response):
        
        #extracting users profile links
#        user_links = response.css(".consumer-info::attr(href)").extract()
#        
#        yield scrapy.Request(
#                url=starturl + user_links[0], 
#                callback=self.parse_nationality, 
#                meta={'urls': user_links, 'current_index': 0},
#                dont_filter= True)
        
        #Extracting the content using css selectors
        product = response.css(".multi-size-header__big::text").extract()
        data_type = response.css(".headline__sub-heading::text").extract()
        times = response.css("time::attr(datetime)").extract()
        reviewers = response.css(".consumer-info__details__name::text").extract()
        reviewers = [reviewer.strip() for reviewer in reviewers]
        review_counts = response.css(".consumer-info__details__review-count::text").extract()
        review_counts = [review_count.strip()[0] for review_count in review_counts]
        titles = response.css(".link.link--large.link--dark::text").extract()
        votes = response.css("div[class*=star-rating--medium]").extract()
        votes = [vote[36] for vote in votes]
        comments = response.xpath('//p[@class="review-info__body__text"]').extract()
        comments = [comment[37:-5].replace("<br>"," ").strip() for comment in comments]
        
        #Give the extracted content row wise
        for item in zip(times,reviewers,review_counts,titles,votes,comments):
#            create a dictionary to store the scraped info
            scraped_info = {
                'product' : 'ACER',
                'data_type' : 'review',
                'time' : item[0],
                'reviewer' : item[1],
                'reviewer_review_count' : item[2],
                'title' : item[3],
                'vote' : item[4],
                'comment' : item[5],
                'language' : 'english'
            }
        
        #yield or give the scraped info to scrapy
            yield scraped_info
            
        next_page = response.css(".button.button--primary.next-page::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse,dont_filter=True
            )
            
        
            
#    def parse_nationality(self, response):
#        yield {'nationalities' : response.css(".user-summary-location::text").extract_first(), 'order' : response.meta['current_index']}
#        current_index = response.meta['current_index'] + 1
#        if current_index < len(response.meta['urls']):
#            yield scrapy.Request(
#                url=starturl + response.meta['urls'][current_index], 
#                callback=self.parse_nationality, 
#                meta={'urls': response.meta['urls'], 'current_index': current_index},
#                dont_filter= True)