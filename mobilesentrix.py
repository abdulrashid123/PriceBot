import requests
from BaseSite import Base
from Product import Product
import time

class MobileSentrix:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    @classmethod
    def run_comparison(cls,frame,shared_dict,lock):
        for i,each in enumerate(frame):
            try:
                print(each)
                print("*************Product***********" + str(i + 1) + each['product_title'])
                name = each['name']
                price = float(each['price'])
                url_product = f"https://www.searchanise.com/getwidgets?api_key=1L2b4q3T7a&q={name}&restrictBy%5Bstatus%5D=1&restrictBy%5Bvisibility%5D=3%7C4&maxResults=10&startIndex=0&items=true&pages=true&facets=false&categories=true&suggestions=true&vendors=false&tags=false&pageStartIndex=0&pagesMaxResults=3&categoryStartIndex=0&categoriesMaxResults=3&suggestionsMaxResults=3&union%5Bprice%5D%5Bmin%5D=se_price_0&vendorsMaxResults=3&tagsMaxResults=3&output=jsonp"
                r = requests.get(url_product, headers=Base.HEADERS)
                products = r.json()['items']
                product_lst = []
                for product in products:
                    temp = {}
                    product_name = product['title']
                    bucks = product['price']
                    temp['name'] = product_name
                    temp['price'] = bucks
                    product_lst.append(temp)
                if product_lst:
                    scores_lst = Product.get_product_related(product_lst, name,price)
                    if scores_lst:
                        print(scores_lst)
                        key = (name, price)
                        with lock:
                            value = shared_dict[key]
                            value[1] = scores_lst
                            shared_dict[key] = value
                            # print("stopped")
                            # return
                if i % 10 == 0:
                    time.sleep(10)
            except Exception as e:
                print(e)
                time.sleep(10)
