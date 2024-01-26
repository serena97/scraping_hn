from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def scrape_page():
    parentPropertyCards = html_parsed.find_all('div', class_='propertyCard')
    for rightmove_property in parentPropertyCards:
       price = rightmove_property.find(class_='propertyCard-priceValue').text
       property_info = rightmove_property.find("div", class_="property-information")
       house_type = property_info.find("span", class_="text").text
       bedrooms = property_info.find("span", class_="bed-icon").find("title").text
       bedrooms_stripped = int(bedrooms.replace(' bedrooms','').replace(' bedroom',''))
       stripped_price = int(price.replace("£", "").replace(",", ""))
       data_obj.append({'price': stripped_price, 'property_type': house_type, 'bedrooms': bedrooms_stripped})
    
    
    
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
    scrape_page()
    next_button = driver.find_element(By.CLASS_NAME, "pagination-direction--next")
    next_button.click()
    print(data_obj)