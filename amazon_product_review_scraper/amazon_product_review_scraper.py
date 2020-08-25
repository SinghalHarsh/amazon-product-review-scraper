# Importing packages
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
import math
from tqdm.auto import tqdm
from random import choice

# to ignore SSL certificate errors
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# random user-agent
from fake_useragent import UserAgent
ua = UserAgent(cache=False, use_cache_server=False)


class amazon_product_review_scraper:
    
    def __init__(self, amazon_site, product_id, sleep_time=1, start_page=1, end_page=None):
        
        # url
        self.url = "https://www." + amazon_site + "/dp/product-reviews/" + product_id + "?pageNumber={}"
        self.sleep_time = sleep_time
        self.reviews_dict = {"date_info":[], "name":[], "title":[], "content":[], "rating":[]}
        
        self.proxies = self.proxy_generator()        
        self.max_try = 10
        self.ua = ua.random
        self.proxy = choice(self.proxies)
        
        self.start_page = start_page
        if (end_page == None):
            self.end_page = self.total_pages()
        else:
            self.end_page = min(end_page, self.total_pages())
        

    #
    def total_pages(self):
        
        response = self.request_wrapper(self.url.format(1))
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ## TODO if else
        content = soup.find_all("span", {"data-hook": "cr-filter-info-review-count"})
        total_reviews = int(content[0].contents[0].split(' ')[-2])
        
        print ("Total reviews: {}".format(total_reviews), flush=True)
        
        total_pages = math.ceil(total_reviews/10)
        return total_pages

 
    # MAIN FUNCTION
    def scraper(self):

        print ("Started!", flush=True)
        print ("Total pages: {}".format(self.end_page), flush=True)

        for page in tqdm(range(self.start_page, self.end_page+1)):
            status = self.page_scraper(page)
            #
            time.sleep(self.sleep_time)

        print ("Completed!")

        # returning df
        return pd.DataFrame(self.reviews_dict)

    
    # page scrapper
    def helper(self, content, tag, parameter_key, parameter_value):
        attribute_lst = []
        attributes = content.find_all(tag, {parameter_key: parameter_value})
        for attribute in attributes:
            attribute_lst.append(attribute.contents[0])
        return attribute_lst

    def page_scraper(self, page):
        
        try:

            response = self.request_wrapper(self.url.format(page))   

            # parsing content
            soup = BeautifulSoup(response.text, 'html.parser')
            ## reviews section
            reviews = soup.findAll("div", {"class":"a-section review aok-relative"})
            ## parsing reviews section
            reviews = BeautifulSoup('<br/>'.join([str(tag) for tag in reviews]), 'html.parser')

            ## 1. title
            titles = reviews.find_all("a", class_="review-title")
            title_lst = []
            for title in titles:
                title_lst.append(title.find_all("span")[0].contents[0])

            ## 2. name
            name_lst = self.helper(reviews, "span", "class", "a-profile-name")

            ## 3. rating
            rating_lst = self.helper(reviews, "span", "class", "a-icon-alt")

            ## 4. date
            date_lst = self.helper(reviews, "span", "data-hook", "review-date")   

            ## 5. content
            contents = reviews.find_all("span", {"data-hook":"review-body"})
            content_lst = []
            for content in contents:
                text_ = content.find_all("span")[0].get_text("\n").strip()
                text_ = ". ".join(text_.splitlines())
                text_ = re.sub(' +', ' ', text_)
                content_lst.append(text_)

            # adding to the main list
            self.reviews_dict['date_info'].extend(date_lst)
            self.reviews_dict['name'].extend(name_lst)
            self.reviews_dict['title'].extend(title_lst)
            self.reviews_dict['content'].extend(content_lst)
            self.reviews_dict['rating'].extend(rating_lst)

        except:
            print ("Not able to scrape page {}".format(page), flush=True)
    
    
    # wrapper around request package to make it resilient
    def request_wrapper(self, url):
        
        while (True):
            # amazon blocks requests that does not come from browser, therefore need to mention user-agent
            response = requests.get(self.url, verify=False, headers={'User-Agent': self.ua}, proxies=self.proxy)
            
            # checking the response code
            if (response.status_code != 200):
                raise Exception(response.raise_for_status())
            
            # checking whether capcha is bypassed or not (status code is 200 in case it displays the capcha image)
            if "Robot Check" in response.text:
                time.sleep(self.sleep_time)
                
                if (self.max_try == 0):
                    raise Exception("CAPTCHA is not bypassed")
                else:
                    self.max_try -= 1
                    self.ua = ua.random
                    self.proxy = choice(self.proxies)
                    continue
                
            self.max_try = 5
            break
            
        return response
    
    # random proxy generator
    def proxy_generator(self):
        proxies = []
        response = requests.get("https://sslproxies.org/")
        soup = BeautifulSoup(response.content, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({
                'ip':   row.find_all('td')[0].string,
                'port': row.find_all('td')[1].string
            })

        proxies_lst = [{'http':'http://'+proxy['ip']+':'+proxy['port']} for proxy in proxies]
        return proxies_lst
    
## Important commands:

# 1. display html
# from IPython.core.display import display, HTML
# display(HTML('<h1>Hello, world!</h1>'))

# 2. check request header
# url = 'http://whatismyheader.com/'