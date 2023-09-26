import requests
from BaseSite import Base
from Product import Product
from bs4 import BeautifulSoup
import re
import time

class PhoneLcd:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    @classmethod
    def run_comparison(cls,frame,shared_dict,lock):
        for i, each in enumerate(frame):
            try:
                print("*************Product***********" + str(i + 1) + each['product_title'])
                print(each)
                name = each['name']
                product_title = each['product_title']
                price = float(each['price'])
                if product_title:
                    url_product = f"https://www.phonelcdparts.com/catalogsearch/result/?q={product_title}"
                else:
                    url_product = f"https://www.phonelcdparts.com/catalogsearch/result/?q={name}"
                print(url_product, product_title)
                r2 = requests.get(url_product, headers=cls.HEADERS)
                soup = BeautifulSoup(r2.text, 'html.parser')
                products = soup.find_all("a", attrs={'class': "product-item-link"})
                product_prices = soup.find_all('span', attrs={'class': 'price'})
                product_lst = []
                for product, product_price in zip(products, product_prices):
                    temp = {}
                    product_name = product.get_text(strip=True)
                    bucks = Base.extract_float_number(product_price.get_text(strip=True))
                    temp['name'] = product_name
                    temp['price'] = bucks
                    product_lst.append(temp)
                if product_lst:
                    scores_lst =Product.get_product_related(product_lst, name,price)
                    if scores_lst:
                        print(scores_lst)
                        key = (name, price)
                        with lock:
                            value = shared_dict[key]
                            value[2] = scores_lst
                            shared_dict[key] = value
                            # print("stopped")
                            # return
        #                 return scores_lst
                if i % 10 == 0:
                    time.sleep(10)
            except Exception as e:
                print(e)
                time.sleep(10)