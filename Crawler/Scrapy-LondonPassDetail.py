import scrapy
import json

url_list = []
fileMain = open("LondonPassAttractions.csv", "r")
for linea in fileMain.readlines():
    url_list.append((linea[252:502].strip()))
fileMain.close()

attractions_items=[]

class LondonPassItemSpider(scrapy.Spider):
    name = "TowerOfLondon"
    start_urls = url_list

    def parse(self, response):
        attraction_name = response.xpath('//div[@id="attraction_header_info"]/h1/span/text()').get()
        attraction_name = ''.join(e for e in attraction_name if e.isalnum() or e == " ")
        attraction_description = response.xpath('//div[@id="attraction_header_info"]/p/text()').get()
        if attraction_description == None or len(attraction_description)==0:
            attraction_description = response.xpath('//div[@id="attraction_header_info"]/p/span/text()').get()
        if attraction_description == None or len(attraction_description)==0:
            attraction_description = response.xpath('//div[@id="attraction_header_info"]/p/strong/text()').get()
        if attraction_description == None or len(attraction_description)==0:
            attraction_description = ""
        attraction_description = ''.join(e for e in attraction_description if e.isalnum() or e == " ")
        ul_list =  response.xpath('//div[@id="attraction_map_left"]/ul/li').getall()
        if len(ul_list)>0:
            attraction_location = ''.join(e for e in ul_list[0] if e.isalnum() or e == " ") 
            attraction_location = attraction_location[ul_list[0].find('</strong>')+len('</strong>'):ul_list[0].find('</li>')]
        else:
            attraction_location = ""
        
        if len(ul_list)>1:
            attraction_station = ''.join(e for e in ul_list[1] if e.isalnum() or e == " ") 
            attraction_station = attraction_station[ul_list[1].find('</strong>')+len('</strong>'):ul_list[1].find('</li>')]
        else:
            attraction_station = ""
            
        if len(ul_list)>2:            
            attraction_busstop = ''.join(e for e in ul_list[2] if e.isalnum() or e == " ") 
            attraction_busstop = attraction_busstop [ul_list[2].find('</strong>')+len('</strong>'):ul_list[2].find('</li>')]
        else:
            attraction_busstop = ""
            
        if len(ul_list)>3:                        
            attraction_tourbusstop = ''.join(e for e in ul_list[3] if e.isalnum() or e == " ") 
            attraction_tourbusstop = attraction_tourbusstop [ul_list[3].find('</strong>')+len('</strong>'):ul_list[3].find('</li>')]
        else:
            attraction_tourbusstop = ""
        
        attraction = {"Name": attraction_name,
                      "Description": attraction_description,
                      "Location": attraction_location,
                      "Station": attraction_station,
                      "BusStop": attraction_busstop,
                      "TourBusStop": attraction_tourbusstop
                      }
        attractions_items.append(attraction)
            

from scrapy.crawler import CrawlerProcess


process = CrawlerProcess({
    'USER_AGENT': 'Google SEO Bot'
})

process.crawl(LondonPassItemSpider)
process.start()

fileChild = open('LondonPassAttractionsInfo.csv', 'w')

linea = ""
for r in attractions_items:
    linea =  "\"{}\"||\"{}\"||\"{}\"||\"{}\"||\"{}\"||\"{}\"".format(r["Name"].strip(), r["Description"].strip(), r["Location"].strip(), r["Station"].strip(), r["BusStop"].strip(), r["TourBusStop"].strip())
    print(linea.encode('utf-8'), file=fileChild)
fileChild.close()
