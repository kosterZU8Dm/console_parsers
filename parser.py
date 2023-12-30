import requests
import pymongo
from datetime import datetime, date, time
import fake_useragent
from bs4 import BeautifulSoup

url = "https://www.belconsole.by/PS5-Playstation-5/igrovye-pristavki/"
user = fake_useragent.UserAgent().random
header = {
    'user-agent': user
}
response = requests.get(url, headers=header)
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
current_db = db_client["belconsole_dot_by"]
collection = current_db["ps5"]

all_ps5_items = []

def get_price(url):
    soup = BeautifulSoup(response.text, "lxml")
    block = soup.find("div", class_="section-main__products")
    all_products = block.find_all("div", class_="ok-product__main")
    for x in all_products:
        product_name = x.find("div", class_="product-name").text.strip()
        old_price = x.find("span", class_="old-price").text
        discount_value = x.find("span", class_="discount-value").text
        current_price = x.find("span", class_="current-price").text
        ps5_item = {
            "product_name": product_name,
            "old_price": old_price,
            "discount_value": discount_value,
            "current_price": current_price,
            "datetime": formatted_datetime
        }
        all_ps5_items.append(ps5_item)
    
    result = collection.insert_many(all_ps5_items)
    print("IDs вставленных документов:", result.inserted_ids)
        
get_price(url)