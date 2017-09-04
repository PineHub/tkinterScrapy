# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class urlMap(scrapy.Item):
	searching = scrapy.Field()  #spider still searching through urls for keyword
	foundTarget = scrapy.Field()    #spider found keyword
	reachedMax = scrapy.Field()	#not used in this version of project, use command line instead
	url = scrapy.Field()    
	scrapeTarget = scrapy.Field()  #used in keyword_search spider to hold keyword
	urlDict = scrapy.Field()       #the name of dictionary output to to into JSON file (ie 'searching' or 'foundTarget')
	targetNode = scrapy.Field()    #text containing the keyword
