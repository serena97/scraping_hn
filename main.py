import httpx
from prefect import flow, task
from bs4 import BeautifulSoup
import requests
import json

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
    
    print(final_obj[2])

    
    
@flow(log_prints=True)
def scraping():
    """
    Scrape https://news.ycombinator.com/ask every 24 hours 
    """
    urls_list = get_urls()
    comments = get_comments(urls_list)
    

if __name__ == "__main__":
    scraping()
