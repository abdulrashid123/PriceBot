import requests
from BaseSite import Base
from Product import Product
import time

class Brosphone:
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
                url_product = f"https://www.brosphoneparts.com/search?type=product&options%5Bprefix%5D=last&options%5Bunavailable_products%5D=show&q={name}"
                r = requests.get(url_product, headers=Base.HEADERS)
                soup = Base.get_soup(r.text)
                products = soup.find_all('a', attrs={"class", "product-item__title text--strong link"})
                product_lst = []
                for product in products:
                    temp = {}
                    product_name = product.get_text(strip=True)
                    bucks = 0
                    try:
                        bucks = Base.extract_float_number(
                            product.next_sibling('span', attrs={"class": ""})[0].get_text(strip=True).replace("$", ""))
                    except Exception as e:
                        print(e)
                        print(product.next_sibling('span', attrs={"class": ""}))
                    temp['name'] = product_name
                    temp['price'] = bucks
                    product_lst.append(temp)
                if product_lst:
                    scores_lst = Product.get_product_related(product_lst, name,price)
                    if scores_lst:
                        print(scores_lst)
                        key = (name,price)
                        with lock:
                            value = shared_dict[key]
                            value[0] = scores_lst
                            shared_dict[key] = value
                        # print("stopped")
                        # return
                if i % 10 == 0:
                    time.sleep(10)
            except Exception as e:
                print(e)
                time.sleep(10)
