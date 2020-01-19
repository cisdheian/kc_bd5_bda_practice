import scrapy
import json

attractions_main = []
url_links = []


class LondonPassSpider(scrapy.Spider):
    name = 'LondonPass'
    start_urls = ['https://www.londonpass.com/london-attractions/']

    def parse(self, response):
        for article in response.css('article'):
            attraction_name = article.css('h3 ::text').extract_first().strip()
            attraction_url = article.css('a').xpath('@href').extract_first()
            if attraction_url is not None:
                attraction_url = attraction_url.strip()
            attraction = {"Name": attraction_name, "Url": attraction_url}
            attractions_main.append(attraction)




from scrapy.crawler import CrawlerProcess

# optional
processMain = CrawlerProcess({
    'USER_AGENT': 'Google SEO Bot'
})



processMain.crawl(LondonPassSpider)
processMain.start()

fileMain = open('LondonPassAttractions.csv', 'w')

for r in attractions_main:
    print("{:250s}||{:250s}".format(r["Name"].strip(), 'https://www.londonpass.com'+r["Url"]).strip(), file=fileMain)
    
fileMain.close()


