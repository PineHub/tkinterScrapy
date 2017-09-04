import  scrapy
import string
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from keywordSearch.items import urlMap
from scrapy.selector import Selector
from w3lib.html import remove_tags



class MySpider(CrawlSpider):
    name = 'keyword_search'        #name of spider
	#allowed_domains = ['ikea.com']
	#start_urls = ['http://www.washington.edu']
    def __init__(self, *args, **kwargs):
		super(MySpider, self).__init__(*args, **kwargs)

		self.start_urls = [kwargs.get('start_url')]  #takes user input at command line for beginning url
		self.scrapeTarget = [kwargs.get('find_word')]  #takes at command line target word
	
    rules = [(Rule(SgmlLinkExtractor(), callback='parse_url', follow=True, process_links=None)),

	]


    def parse_url(self, response):
		
		xSrchString = "//*[contains(text(), "+str(self.scrapeTarget)[1:-1]+")]"  #find your keyword, converted from dictionary format to string
		item = urlMap()
		closeable = 0	#conditional statement will switch this to '1' when target found.
		if (response.xpath(xSrchString)):
			#yield end_parse(response)
			item['urlDict'] = {'foundTarget' : response.url}   #your url with the target keyword is here
			item['targetNode'] = {remove_tags(response.xpath(xSrchString).extract_first())}  #your text containing your keyword is here, tags removed a much as possible
			
			
			closeable = 1
			#print("i'm in parse url scrape target is " + '//*[contains(text(), '+str(self.scrapeTarget)[1:-1]+')]' + "\n")
			yield item
			
		elif closeable != 1:
			item['urlDict'] = {'searching' : response.url}   #record url that didn't contain the keyword
			yield item
			
		if closeable == 1:
			raise scrapy.exceptions.CloseSpider(reason='Target_Found')   #close down spider
			

	
