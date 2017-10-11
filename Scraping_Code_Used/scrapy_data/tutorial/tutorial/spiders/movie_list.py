import scrapy


class MoviesSpider(scrapy.Spider):

    name = 'mlist_data'

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
        
        L_movie_titles = response.xpath('//td/table[1]/tr/td[2]/font/a/b/text()').extract()
        l=len(L_movie_titles)
        L_Adj_Gross = response.xpath('//td[@ align="right"]/font[@size="2"]/b/text()').extract()[l+4:(2*l+5)]
        L_R_Date = response.xpath('//tr/td[@ align="right"]/font[@size="2"]/a/text()').extract()[:l]
        #L_Gross = response.xpath('//tr/td[@ align="right"]/font[@size="2"]/text()').extract()[-l-2:-2]
        for i in range(len(L_movie_titles)):    #goes through each movie in the franchise table
            yield {
                'F_Movie_Title': L_movie_titles[i],
                'F_Adj_Gross': L_Adj_Gross[i],
                'F_R_Date': L_R_Date[i],
                #'F_Gross': L_Gross[i]
                
            }
           
    '''
    def parse_movies(self, response):     #parses and extracts info from one movie page at a time

        url = response.request.meta['url']
        genre = response.xpath('//td[@valign= "top"]/b/text()').extract()[0]
        run_time = response.xpath('//td[@valign= "top"]/b/text()').extract()[1]
        mpaa = response.xpath('//td[@valign= "top"]/b/text()').extract()[2]
        budget = response.xpath('//td[@valign= "top"]/b/text()').extract()[3]
        Title = response.xpath('//td/font/b/text()').extract()[0]
        Domestic_Gross = response.xpath('//td/font/b/text()').extract()[1]
        Genre2 = response.xpath('//td/font[@size="2"]/a/text()').extract()[2]
        Director = response.xpath('//td/font[@size="2"]/a/text()').extract()[1]
        F_Series =response.xpath('//td/font[@size="2"]/a/b/text()').extract()[1]
        W_Theatre = response.xpath('//div[@ class="mp_box_content"]/table/tr/td/text()').extract()[5] 
        Op_Wkend = response.xpath('//div[@ class="mp_box_content"]/table/tr/td/text()').extract()[1] 
        Rel_Date = response.xpath('//td[@ valign="top"]/b/nobr/a/text()').extract()  
        S_Rank =response.xpath('//td[@ align="center"]/font[@ size="2"]/b/text()').extract()  
          
        yield {
            'url': url,
            'genre': genre,
            'run_time': run_time,
            'rating': mpaa,
            'budget': budget,
            'F_Series': F_Series,
            'Director': Director, 
            'Release Date': Rel_Date, 
            'Genre2':Genre2,
            'Title':Title,
            'Series Rank': S_Rank,
            'Domestic Gross':Domestic_Gross,
            #'Adjusted Domestic Gross':
            'Opening Weekend': Op_Wkend,
            'Widest Release':W_Theatre
        }
      '''