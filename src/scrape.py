import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, uuid
from temporalio import activity
import redis, json
import logging

logger = logging.getLogger(__name__)

from config import REDIS_HOST, REDIS_PORT, REDIS_DB

custom_headers = {
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
}

def get_soup(url):
    response = requests.get(url, headers=custom_headers, auth=(os.getenv('AMAZON_USERNAME'), os.getenv('AMAZON_PASSWORD')) )
    if response.status_code != 200:
        logger.error(f"Error in getting webpage: {response.status_code}")
        exit(-1)

    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_reviews(soup):
    review_elements = soup.select("div.review")
    scraped_reviews = []

    for review in review_elements:
        r_author_element = review.select_one("span.a-profile-name")
        r_author = r_author_element.text if r_author_element else None

        r_rating_element = review.select_one("i.review-rating")
        r_rating = r_rating_element.text.replace("out of 5 stars", "") if r_rating_element else None

        r_title_element = review.select_one("a.review-title")
        r_title_span_element = r_title_element.select_one("span:not([class])") if r_title_element else None
        r_title = r_title_span_element.text if r_title_span_element else None

        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None

        r_date_element = review.select_one("span.review-date")
        r_date = r_date_element.text if r_date_element else None

        r_verified_element = review.select_one("span.a-size-mini")
        r_verified = r_verified_element.text if r_verified_element else None

        r_image_element = review.select_one("img.review-image-tile")
        r_image = r_image_element.attrs["src"] if r_image_element else None

        r = {
            "author": r_author,
            "rating": r_rating,
            "title": r_title,
            "content": r_content,
            "date": r_date,
            "verified": r_verified,
            "image_url": r_image
        }

        scraped_reviews.append(r)

    return scraped_reviews

@activity.defn
async def scrape(item):
    #activity.logger.info("Scrape activity on parameter %s" % item)
    page = 1
    dataframes = pd.DataFrame()
    while True:
        search_url = "https://www.amazon.com/product-reviews/%s/ref=cm_cr_arp_d_paging_btm_next_%d?pageNumber=%d" % (item, page, page)
        logger.info("Item: %s, Scraping: %s" % (item, search_url) )
        soup = get_soup(search_url)
        data = get_reviews(soup)
        df = pd.DataFrame(data=data)
        if df.size == 0:
            break
        dataframes = pd.concat([dataframes,df], ignore_index=True)
        page = page+1

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    itemkeys = list()
    for row in dataframes.itertuples(index=False):
        try:
            star = row.rating
            title = row.title
            content = row.content
            key = item+"-"+str(uuid.uuid4())[:8]
            data = {
                "star": star,  
                "title": title,  
                "content": content  
            }
            value_str = json.dumps(data)
            r.set(key, value_str)
            itemkeys.append(key)
        except Exception as e:
            logger.exception("Item: %s, Pandas row exception")
            return 0

    return itemkeys
