import httpx
from prefect import flow, task
from bs4 import BeautifulSoup
import requests
import json
import psycopg2
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup

conn = psycopg2.connect(
   database="my_database", user='user', password='password', host='localhost', port= '5433'
)
cursor = conn.cursor()


@task
def get_urls():
    """Get info about a repo - will retry twice after failing"""
    url = "https://news.ycombinator.com/ask"
    page = requests.get(url)
    html = BeautifulSoup(page.content, "html.parser")
    
    parentElements = html.find_all('span', class_='titleline')
    urls = []
    for el in parentElements:
        url_append = el.find('a').get('href')
        title = el.find('a').text
        new_url = 'https://news.ycombinator.com/' + url_append
        urls.append({'url': new_url, 'title': title})
    
    return urls

@task
def get_comments(urls):
    """_summary_
        Scrape the body of the question and all the comments
    """
    final_obj = []
    for obj in urls:
        time.sleep(3)
        page = requests.get(obj.get('url'))
        html = BeautifulSoup(page.content, "html.parser")
        body = html.find('div', class_='toptext')
        if body is not None:
            body = body.text
        else:
            body = ''
        comments = html.find_all('div', class_='comment')
        comments_txt = [comment.text for comment in comments]
        final_obj.append({
            'url': obj.get('url'),
            'title': obj.get('title'),
            'body': body,
            'comments': comments_txt
        })
        
    return final_obj


@task
def write_to_db(final_obj):
    query = """
    INSERT INTO web_data (url, title, body, comments)
    VALUES (%s, %s, %s, %s);
    """
    print(f"writing {len(final_obj)} rows to postgresql")
    for row in final_obj:
        data = (row['url'], row['title'], row['body'], row['comments'])
        cursor.execute(query, data)
        conn.commit()

@task
def write_to_db_rightmove(final_obj):
    query = """
    INSERT INTO rightmove (price, property_type, bedrooms)
    VALUES (%s, %s, %s);
    """
    print(f"writing {len(final_obj)} rows to postgresql")
    for row in final_obj:
        data = (row['price'], row['property_type'], row['bedrooms'])
        cursor.execute(query, data)
        conn.commit()
    
@flow(log_prints=True, name='hackernews')
def scraping():
    """
    Scrape https://news.ycombinator.com/ask every 24 hours 
    """
    print('starting to scrape')
    urls_list = get_urls()
    final_obj = get_comments(urls_list)
    write_to_db(final_obj)

@task
def get_properties():
    """
    Scrape https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=OUTCODE%5E1865&index=24&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords=
    and save average price of house to Fact Table in PostgreSQL
    """
    options = Options() # Create an Options object
    options.add_argument("--headless") # Make it headless
    options.add_argument("--no-sandbox") # Disable the limits protecting from potential viruses
    options.add_argument("--disable-dev-shm-usage") # don't use disk memory
    service = Service(ChromeDriverManager().install()) # Install the ChromeDriver if not already present
    url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=OUTCODE%5E1865&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='
    data_obj = []
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(url)
        html = driver.page_source
        html_parsed = BeautifulSoup(html, "html.parser")
        parentPropertyCards = html_parsed.find_all('div', class_='propertyCard')
        for rightmove_property in parentPropertyCards:
            price = rightmove_property.find(class_='propertyCard-priceValue').text
            property_info = rightmove_property.find("div", class_="property-information")
            house_type = property_info.find("span", class_="text").text
            bedrooms = property_info.find("span", class_="bed-icon").find("title").text
            bedrooms_stripped = int(bedrooms.replace(' bedrooms','').replace(' bedroom',''))
            stripped_price = int(price.replace("£", "").replace(",", ""))
            data_obj.append({'price': stripped_price, 'property_type': house_type, 'bedrooms': bedrooms_stripped})
    return data_obj
    
    
@flow(log_prints=True, name='rightmove')
def scraping_rightmove():
    properties = get_properties()
    write_to_db(properties)
    

if __name__ == "__main__":
    scraping.serve(name="hn-rightmove-deployment",cron="15 0 * * *")
