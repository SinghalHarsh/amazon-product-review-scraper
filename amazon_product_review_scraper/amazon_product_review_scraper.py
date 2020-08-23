# Importing packages
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time

# to ignore SSL certificate errors
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Scrapper
def helper(content, tag, parameter_key, parameter_value):
    attribute_lst = []
    attributes = content.find_all(tag, {parameter_key: parameter_value})
    for attribute in attributes:
        attribute_lst.append(attribute.contents[0])
    return attribute_lst

def scraper(url):
    
    # amazon blocks requests that does not come from browser, therefore need to mention user-agent
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
    response = requests.get(url, verify=False, headers=headers)
    
    # checking  if an error has occurred 
    if (response.status_code != 200):
        raise Exception(response.raise_for_status())
    

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
    name_lst = helper(reviews, "span", "class", "a-profile-name")
    
    ## 3. rating
    rating_lst = helper(reviews, "span", "class", "a-icon-alt")
    
    ## 4. date
    date_lst = helper(reviews, "span", "data-hook", "review-date")   
    
    ## 5. content
    contents = reviews.find_all("span", {"data-hook":"review-body"})
    content_lst = []
    for content in contents:
        text_ = content.find_all("span")[0].get_text("\n").strip()
        text_ = ". ".join(text_.splitlines())
        text_ = re.sub(' +', ' ', text_)
        content_lst.append(text_)
    
    # adding to the main list
    reviews_dict['date_info'].extend(date_lst)
    reviews_dict['name'].extend(name_lst)
    reviews_dict['title'].extend(title_lst)
    reviews_dict['content'].extend(content_lst)
    reviews_dict['rating'].extend(rating_lst)
    
    # checking whether scrapping is completed
    if (len(title_lst) == 0):
        return "completed"
    else:
        return "running"

def amazon_review_scraper(amazon_site, product_id, sleep_time=1):
    
    # url
    url = "https://www." + amazon_site + "/dp/product-reviews/" + product_id + "?pageNumber={}"
        
    #
    global reviews_dict
    reviews_dict = {"date_info":[], "name":[], "title":[], "content":[], "rating":[]}
    
    print ("Started!")
    
    page = 1
    while(True):
        print ("Scrapping page: {}".format(page), end="\r")
        status = scraper(url.format(page))

        if (status == "completed"):
            break
        page += 1
        
        time.sleep(sleep_time)
        
    print ()
    print ("Completed!")
        
    # creating df
    reviews_df = pd.DataFrame(reviews_dict)
    return reviews_df