# Amazon Product Review Scraper
Python package to scrape product review data from amazon

## Quickstart

    pip install amazon-product-review-scraper
    
    from amazon_product_review_scraper import amazon_product_review_scraper
    review_scraper = amazon_product_review_scraper(amazon_site="amazon.in", product_id="B07X6V2FR3")
    reviews_df = review_scraper.scrape()
    reviews_df.head(5)
    
![quickstart](https://github.com/SinghalHarsh/amazon-product-review-scraper/blob/master/tutorials/quickstart.png)

## Parameters
    
    
