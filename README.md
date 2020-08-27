# Amazon Product Review Scraper
Python package to scrape product review data from amazon

## Quickstart

```
pip install amazon-product-review-scraper
```
        
```
from amazon_product_review_scraper import amazon_product_review_scraper
review_scraper = amazon_product_review_scraper(amazon_site="amazon.in", product_asin="B07X6V2FR3")
reviews_df = review_scraper.scrape()
reviews_df.head(5)
```
    
<kbd>
  <img src="https://github.com/SinghalHarsh/amazon-product-review-scraper/blob/master/tutorials/quickstart.png">
</kbd>

## Parameters

#### ```amazon_site```
        
        **Examples**: amazon.in, amazon.com, amazon.co.uk
   
   

   
#### ```product_asin```
   
        Product ASIN [(Amazon Standard Identification Number)](https://www.nchannel.com/blog/amazon-asin-what-is-an-asin-number/)
        
        An ASIN is a 10-character alphanumeric unique identifier that is assigned to each product on amazon.
        
        **Examples**:
        * https<span>://ww</span>w.amazon.i<span>n/Grand-Theft-Auto-V-PS4/dp/<code><b><ins>B00L8XUDIC</ins></b></code>/ref=sr_1_1
        * http</span>s://ww<span>w.amazon.</span>in/Renewed-Sony-Cybershot-DSC-RX100-Digital/dp/<code><b><ins>B07XRVR9B9</ins></b></code>/ref=lp_20690678031_1_14?srs=20690678031&ie=UTF8&qid=1598553991&sr=8-14
  
   
#### ```sleep_time``` (Optional)
   
        Number of seconds to wait before scraping the next page.
        
        (Amazon might intervene with CAPTCHA if receives too many requests in a small period of time)
   
#### ```start_page``` (Optional)
#### ```end_page``` (Optional)
