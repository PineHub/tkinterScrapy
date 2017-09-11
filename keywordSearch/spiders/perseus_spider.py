import scrapy
import string
import turtle
import random
import datetime
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from keywordSearch.items import urlMap
from scrapy.selector import Selector
from w3lib.html import remove_tags


def spiderVisual(linkLength, dictionaryLength, found):
    now = datetime.datetime.now()
    wn = turtle.Screen()  # creates a graphics window
    width = wn.window_width()
    height = wn.window_height()
    wn.colormode(255)

    randx = random.randrange((width / 2) * -1, width / 2)   #makes the turtle draw towards random locations at the edge of the window
    randy = random.randrange((height / 2) * -1, height / 2)
    randStart = random.randrange(1, 5)

    pete = turtle.Turtle()  # create a turtle named pete
    pete.pensize(5)    # change the pen size

    revisedLinkLength = linkLength

    if revisedLinkLength > 255:
        revisedLinkLength = 255   #shorten the length of the link if its greater than 255 characters for the purposes of the visualizer, whose color pallet doesn't go beyond 255

    # print("now minute and now second: ", (now.minute + now.second) *2)
    # print("dictionalry length random: ", random.randrange(dictionaryLength, 256))
    # print("revisedLinkLength: ", revisedLinkLength)

    dictionaryDifference = random.randrange(dictionaryLength, 256)

    if dictionaryDifference < 1:
        dictionaryDifference = dictionaryDifference + 1

    pete.pencolor((now.minute + now.second) * 2, dictionaryDifference, revisedLinkLength)  # colors based time of day in minutes and seconds, size of dictionary (pages searched), length of hyperlink
    loc = pete.position()  # location of pete

    #move turtle to random edges of screen
    if loc == (0, 0) and found == 0:
        if randStart == 1:
            pete.goto(randx, (height / 2) * -1)
        elif randStart == 2:
            pete.goto(randx, (height / 2))
        elif randStart == 3:
            pete.goto(((width) / 2) * -1, randy)
        elif randStart == 4:
            pete.goto(((width) / 2), randy)

    if found == 1 and loc == (0, 0):
        print("found is 1!!")
        pete.begin_fill()
        if randStart == 1:
            pete.goto(randx, (height / 2) * -1)
        elif randStart == 2:
            pete.goto(randx, (height / 2))
        elif randStart == 3:
            pete.goto(((width) / 2) * -1, randy)
        else:
            pete.goto(((width) / 2), randy)
        pete.end_fill()
        pete.done()


class MySpider(CrawlSpider):
    name = 'keyword_search'  # name of spider

    # allowed_domains = ['ikea.com']
    # start_urls = ['http://www.washington.edu']
    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]  # takes user input at command line for beginning url
        self.scrapeTarget = [kwargs.get('find_word')]  # takes at command line target word

    rules = [(Rule(SgmlLinkExtractor(), callback='parse_url', follow=True, process_links=None)),

             ]

    def parse_url(self, response):

        xSrchString = "//*[contains(text(), " + str(self.scrapeTarget)[
                                                1:-1] + ")]"  # find your keyword, converted from dictionary format to string
        item = urlMap()
        closeable = 0  # conditional statement will switch this to '1' when target found.
        if response.xpath(xSrchString) and closeable == 0:
            # yield end_parse(response)
            item['urlDict'] = {'foundTarget': response.url}  # your url with the target keyword is here
            item['targetNode'] = {remove_tags(response.xpath(
                xSrchString).extract_first())}  # your text containing your keyword is here, tags removed a much as possible

            closeable = 1
            # print("i'm in parse url scrape target is " + '//*[contains(text(), '+str(self.scrapeTarget)[1:-1]+')]' + "\n")

            yield item


        elif closeable != 1:
            item['urlDict'] = {'searching': response.url}  # record url that didn't contain the keyword
            spiderVisual(len(response.url), len(item['urlDict']), 0)

            if closeable == 1:  # found keyword, ok to close
				spiderVisual(len(response.url), len(item['urlDict']), 1)

            yield item



        if closeable == 1:
            raise scrapy.exceptions.CloseSpider(reason='Target_Found')  # close down spider


