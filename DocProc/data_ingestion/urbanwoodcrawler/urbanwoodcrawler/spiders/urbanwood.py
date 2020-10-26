    # -*- coding: utf-8 -*-
import sys
import os 
import os
import xlrd
import logging
import pandas as pd

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from bs4 import BeautifulSoup
from bs4.element import Comment

from urbanwoodcrawler.items import UWcrawlerItem

# Logger instance
logging.basicConfig(filename='crawl.log')
logger = logging.getLogger(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))

class UrbanwoodSpider(scrapy.Spider):
    name = 'uwspider'

    # Helper variables
    link_counter = 1
    visited_urls = list()

    # Initializing to visit links. Hardcode (as cannot pass as an argument variable)
    df = pd.read_excel(dir_path + '/../../../data/Websites.xlsx')
    visit_urls = df['URL'].dropna().tolist()
    print (visit_urls)

    def start_requests(self):
    	'''
    	Initiates crawling
    	'''
    	for url in list(self.visit_urls):
    		# Iterating over copy of urls so as to modify urls

			# Popping visited urls
    		self.visit_urls.remove(url)

    		# Crawling unvisited pages
    		if url not in self.visited_urls:
    			yield scrapy.Request(url, callback=self.parse_first_page)

    def parse_first_page(self, response):
    	'''
    	Function receives crawled page
    	'''
    	# Logging
    	logger.debug('Crawling 1st page link{0} : {1}'.format(self.link_counter, 
    															response.url))
    	# Storing data
    	item = self.store_data(response)  

    	# Parsing response for link extraction
    	soup = BeautifulSoup(response.body, features="lxml")  		   	

    	return item

    def store_data(self, response):
    	'''
    	Prepares item from response body
    	'''
   		# Incrementing link counter
    	self.link_counter += 1

        # Prevent re-crawling of links
    	self.visited_urls.append(response.url)

    	# Parsing response
    	soup = BeautifulSoup(response.body, features="lxml")

    	# Filling item
    	item = UWcrawlerItem()
    	item['link'] = response.url

    	# Getting only visible text from webpage
    	texts = soup.findAll(text=True)
    	visible_texts = filter(UrbanwoodSpider.tag_visible, texts)  
    	item['text'] = " ".join(t.strip() for t in visible_texts) 

    	return item

    def tag_visible(element):
    	'''
    	Getting data from wiki page
    	'''
    	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', 
                                    '[document]']:
    		return False
    	if isinstance(element, Comment):
    		return False

    	return True