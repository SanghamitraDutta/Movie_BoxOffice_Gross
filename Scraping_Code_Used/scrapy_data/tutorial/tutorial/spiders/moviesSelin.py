import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#import requests
import re
#from bs4 import BeautifulSoup

import os
chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


driver = webdriver.Chrome(chromedriver)

class MDetailSpider(scrapy.Spider):

    name = 'movies_data_new'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }
    # Page it begins scraping
    start_urls = [
        'http://www.boxofficemojo.com/franchises/'
    ]
    
    def parse(self, response):
        # Extracts the links of the franchise movie tables from the table of movie links as a list and saves in table below
        table = response.xpath('//div[@id="body"]/table[2]/tr/td[1]/table/tr/td[1]/font/a/@href').extract()   #
        for franchise in table[1:]:   #parse through each row of table except 1st row which is header
            yield scrapy.Request(
                 url='http://www.boxofficemojo.com/franchises' + franchise[1:], #start from 2nd elm in string as 1st'.' not needed
                 callback =self.parse_movie_list,   #calls method below
                 meta={'url': franchise}
            )

    def parse_movie_list(self, response):
        #Extracts table with links to a particular movie franchise
        table = response.xpath('//div[@id="body"]/table[2]/tr/td[1]/table/tr/td/table[1]/tr/td[2]/font/a/@href').extract()
        for movie in table[1:]:    #goes through each movie in the franchise table
            yield scrapy.Request(
                 url='http://www.boxofficemojo.com/' + movie,        
                 callback =self.parse_movies,            #calls method below to extract data from each movie pg
                 meta={'url': movie}
           )
    
    def parse_movies(self, response):     #parses and extracts info from one movie page at a time
        
        url = response.request.meta['url']
        genre = response.xpath('//td[@valign= "top"]/b/text()').extract()[0]
        run_time = response.xpath('//td[@valign= "top"]/b/text()').extract()[1]
        mpaa = response.xpath('//td[@valign= "top"]/b/text()').extract()[2]
        budget = response.xpath('//td[@valign= "top"]/b/text()').extract()[3]
        Title = response.xpath('//td/font/b/text()').extract()[0]
        Domestic_Gross = response.xpath('//td/font/b/text()').extract()[1]
        Director1 = response.xpath('//td/font[@size="2"]/a/text()').extract()[1]
        Director = response.xpath('//td[contains(text(),"Director")]//following-sibling::td/text()').extract_first()
        F_Series =response.xpath('//td/font[@size="2"]/a/b/text()').extract()[1]
        W_Theatre = response.xpath('//div[@ class="mp_box_content"]/table/tr/td/text()').extract()[5]
        NWid_theaters = response.xpath('//td[contains(text(),"Widest")]//following-sibling::td/text()').extract_first()
        Op_Wkend1 = response.xpath('//div[@ class="mp_box_content"]/table/tr/td/text()').extract()[1]
        Rel_Date = response.xpath('//td[@ valign="top"]/b/nobr/a/text()').extract()  
        S_Rank =response.xpath('//td[@ align="center"]/font[@ size="2"]/b/text()').extract()  
        
        driver_url = 'http://www.boxofficemojo.com'+ url 
        driver.get(driver_url)
        
        gross_selector = '//font[contains(text(), "Domestic")]/b'
        NDom_gross = (driver.find_element_by_xpath(gross_selector).text)
        
        inf_adjust_2017_selector = '//select[@name="ticketyr"]/option[@value="2017"]'
        driver.find_element_by_xpath(inf_adjust_2017_selector).click()
        go_button = driver.find_element_by_name("Go")
        go_button.click()   
        gross_selector = '//font[contains(text(), "Domestic ")]/b'
        NAdj_Dom_gross = driver.find_element_by_xpath(gross_selector).text
        
        #response = requests.get(driver_url)
        #soup = BeautifulSoup(response,"lxml")
        '''
        obj = soup.find(text=re.compile("Weekend:"))
        if not obj: 
            Op_Wkend = None
            next_sibling = obj.findNextSibling()
            if next_sibling:    
                Op_Wkend = next_sibling.text 
            else:
                Op_Wkend = None
        '''
        yield {
            'Title':Title,
            'genre': genre,
            'budget': budget,
            'Domestic Gross1':Domestic_Gross,
            'Domestic Gross':NDom_gross,
            'Adj_Dom_Gross': NAdj_Dom_gross,
            'Director1': Director1, 
            'Director': Director, 
            'Widest Release1':W_Theatre,
            'Widest Release:':NWid_theaters,
            'Release Date': Rel_Date, 
            'run_time': run_time,
            'rating': mpaa,  
            'F_Series': F_Series,    
            'Opening Weekend1': Op_Wkend1,
            #'Opening Weekend': Op_Wkend,
            'url': url,
            'Series Rank': S_Rank
        }

'''     
   Step1
   Start_urls  ---> takes the url of page u wish to beign at
   
   Step2
   inspect where u wish to extract from...copy xpath from that position... and in xpath replace * with tag that comes before     [@id="body"] and you get the url below    
   //div[@id="body"]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td[1]/font/a     
   
   Step3
   check output in command line:
   Enter scrapy shell --->
   scrapy shell 'http://www.boxofficemojo.com/franchises/'
   check scrapy outpu ----> 
   response.xpath('//div[@id="body"]/table[2]/tr/td[1]/table/tr/td[1]/font/a/@href').extract()
   
   returns the contents of the table in a list--- links to all movie franchise page ---- save list in variable table
   we need to start from 2nd row in table as 1st row is header
   
   Using for loop go into each link(each list of franchise movie) in table 
   
   Step 4 Open up 1st url on franchises list ---3 ninjas
   
   Commnand line quit earlier using ----> quit()
   Enter scrapy shell for the 3 ninjas page ---->
   scrapy shell 'http://www.boxofficemojo.com/franchises/chart/?id=3ninjas.htm'
   Inspect the table on this page --->
   Find your spot on html
   Go to <a href..> tag just above it copy xpath--->
   //*[@id="body"]/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[1]/tbody/tr[2]/td[2]/font/a
   Repalce * by tag of [@id="body"]... we find it is div---->
   //div[@id="body"]/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/font/a
   remove tbody as having it is not printing contents of table
   add /@href at the end of the above link ---->
   //div[@id="body"]/table[2]/tr/td[1]/table/tbody/tr/td/table[1]/tr[1]/td[2]/font/a/@href
   
   for loop through each movie link ----> go to movie page
   
   Then parse movie data on each movie pg
   
   
   quit()  ----> scrapy shell
   
   go to /Users/sdutta/desktop/wip/scrapy_data/tutorial ----->1st tutorial directory on command line and run command below
  
   scrapy crawl movies_data -o movies.json
   
   scrapy crawl (class name) -o (name of data file).json
''' 
   
   