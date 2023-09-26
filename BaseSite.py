import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import time
import multiprocessing
from multiprocessing import Lock
# from Product import Product

class Base:
    URL = "https://ccpparts.com/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    def __init__(self,cache=False):
        self.cache = True
        self.frame = None
        self.result = pd.DataFrame()

    # @staticmethod
    # def execute_javascript(code):
    #     return js_runtime.eval(code)

    @staticmethod
    def remove_words_in_brackets(name):
        name = re.sub(r'\([^)]*\)', '', name)  # Removes words within parentheses
        name = re.sub(r'\[[^\]]*\]', '', name)  # Removes words within square brackets
        name = re.sub(r'\{[^}]*\}', '', name)  # Removes words within curly braces
        return name.strip()

    @staticmethod
    def get_soup(string):
        return BeautifulSoup(string, 'html.parser')

    @staticmethod
    def extract_float_number(text):
        number = re.search(r'(\d+(\.\d+)?)', text)
        if number:
            return float(number.group())
        else:
            return None


    @staticmethod
    def save_csv(frame,filename):
        frame.to_csv(filename,index=False)


    def run_bot(self,cache=False):
        if cache:
            print("using cache data")
            df = pd.read_csv('base_product.csv')
            df = df.where(pd.notna(df), "")
            frame = df.to_dict('records')
        else:
            frame = self.get_base_site_data()


        self.result = pd.DataFrame(frame)
        del self.result['product_title']
        self.result.to_csv('result.csv',index=False)
        manager = multiprocessing.Manager()
        shared_dict = manager.dict()
        lock = Lock()
        for each in frame:
            name = each['name']
            price = each['price']
            shared_dict[(name,price)] = [0,0,0]
        processes = []
        from brosphone import Brosphone
        from mobilesentrix import MobileSentrix
        from phonelcd import PhoneLcd
        # print(shared_dict)


            # Create a process for each data entry
        p = multiprocessing.Process(target=Brosphone.run_comparison, args=(frame,shared_dict,lock))
        p.start()

        p1 = multiprocessing.Process(target=MobileSentrix.run_comparison, args=(frame, shared_dict, lock))
        p1.start()
        # #
        p2 = multiprocessing.Process(target=PhoneLcd.run_comparison, args=(frame, shared_dict, lock))
        p2.start()
        # # # Wait for all processes to finish
        p.join()
        p1.join()
        p2.join()

        # Print the resulting dictionary


        # print("Shared Dictionary:", shared_dict)
        self.convert_to_html(shared_dict)
        # get 1st website data

    @staticmethod
    def convert_to_html(shared_dict):
        html_table = ""
        dictonary = dict(shared_dict)
        html_table = """
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Price</th>
                <th>Brosphone</th>
                <th>Brosphone Price</th>
            </tr>
            {rows}
        </table>
        """
        table_rows = ""
        for each in dictonary:
            close_row = False
            table_row = f"""
               <tr>
                   <td>{each[0]}</td>
                   <td>{each[1]}</td>
                
                """
            if dictonary[each][0]:
                bros = dictonary[each][0]
                for index,element in enumerate(bros):
                    name = element['name']
                    price = element['price']
                    if index == 0:
                        if each[1] >= price:
                            temp = f"""
                                <td>{name}</td>
                                <td style="background-color: red; color: white;">{price}</td>
                            </tr>
                            """
                        else:
                            temp = f"""
                                    <td>{name}</td>
                                    <td style="background-color: green;">{price}</td>
                                     </tr>
                                    """
                        close_row = True
                        table_row += temp
                        table_rows += table_row
                    else:
                        if each[1] >= price:
                            temp = f"""
                            <tr>
                            <td></td>
                            <td></td>
                            <td>{name}</td>
                            <td style="background-color: red; color: white;">{price}</td>
                            </tr>
                            """
                        else:
                            temp = f"""
                                    <tr>
                                    <td></td>
                                    <td></td>
                                    <td>{name}</td>
                                    <td style="background-color: green;">{price}</td>
                                    </tr>
                                    """
                        table_rows += temp
            if not close_row:
                table_row += """<td></td>
                            <td></td></tr>"""
                table_rows += table_row
        html_table = html_table.format(rows=table_rows)
        with open("Brosphone.html", "w") as html_file:
            html_file.write(html_table)

        html_table = """
                <table border="1">
                    <tr>
                        <th>Name</th>
                        <th>Price</th>
                        <th>MobileSentrix</th>
                        <th>MobileSentrix Price</th>
                    </tr>
                    {rows}
                </table>
                """
        table_rows = ""
        for each in dictonary:
            close_row = False
            table_row = f"""
                       <tr>
                           <td>{each[0]}</td>
                           <td>{each[1]}</td>

                        """
            if dictonary[each][1]:
                bros = dictonary[each][1]
                for index, element in enumerate(bros):
                    name = element['name']
                    price = element['price']
                    if index == 0:
                        if each[1] >= price:
                            temp = f"""
                                <td>{name}</td>
                                <td style="background-color: red; color: white;">{price}</td>
                            </tr>
                            """
                        else:
                            temp = f"""
                                    <td>{name}</td>
                                    <td style="background-color: green;">{price}</td>
                                     </tr>
                                    """
                        close_row = True
                        table_row += temp
                        table_rows += table_row
                    else:
                        if each[1] >= price:
                            temp = f"""
                            <tr>
                            <td></td>
                            <td></td>
                            <td>{name}</td>
                            <td style="background-color: red; color: white;">{price}</td>
                            </tr>
                            """
                        else:
                            temp = f"""
                                    <tr>
                                    <td></td>
                                    <td></td>
                                    <td>{name}</td>
                                    <td style="background-color: green;">{price}</td>
                                    </tr>
                                    """
                        table_rows += temp
            if not close_row:
                table_row += """<td></td>
                                    <td></td></tr>"""
                table_rows += table_row
        html_table = html_table.format(rows=table_rows)
        with open("MobileSentrix.html", "w") as html_file:
            html_file.write(html_table)

        html_table = """
                       <table border="1">
                           <tr>
                               <th>Name</th>
                               <th>Price</th>
                               <th>PhoneLcd</th>
                               <th>PhoneLcd Price</th>
                           </tr>
                           {rows}
                       </table>
                       """
        table_rows = ""
        for each in dictonary:
            close_row = False
            table_row = f"""
                              <tr>
                                  <td>{each[0]}</td>
                                  <td>{each[1]}</td>

                               """
            if dictonary[each][2]:
                bros = dictonary[each][2]
                for index, element in enumerate(bros):
                    name = element['name']
                    price = element['price']
                    if index == 0:
                        if each[1] >= price:
                            temp = f"""
                                <td>{name}</td>
                                <td style="background-color: red; color: white;">{price}</td>
                            </tr>
                            """
                        else:
                            temp = f"""
                                    <td>{name}</td>
                                    <td style="background-color: green;">{price}</td>
                                     </tr>
                                    """
                        close_row = True
                        table_row += temp
                        table_rows += table_row
                    else:
                        if each[1] >= price:
                            temp = f"""
                            <tr>
                            <td></td>
                            <td></td>
                            <td>{name}</td>
                            <td style="background-color: red; color: white;">{price}</td>
                            </tr>
                            """
                        else:
                            temp = f"""
                                    <tr>
                                    <td></td>
                                    <td></td>
                                    <td>{name}</td>
                                    <td style="background-color: green;">{price}</td>
                                    </tr>
                                    """
                        table_rows += temp
            if not close_row:
                table_row += """<td></td>
                                           <td></td></tr>"""
                table_rows += table_row
        html_table = html_table.format(rows=table_rows)
        with open("PhoneLcd.html", "w") as html_file:
            html_file.write(html_table)

    def get_base_site_data(self):
        r = requests.get(self.URL, headers=self.HEADERS)
        soup = self.get_soup(r.text)
        pattern = re.compile(r'globoMenu\d+Item\d+')
        scripts = soup.find_all("script", id=pattern)
        data_product = []
        frame = []
        for script in scripts:
            lst = BeautifulSoup(script.string, 'html.parser')
            product_titles = lst.find("li").find_all("a", attrs={"class": "gm-target"})
            for each in product_titles:
                product = each.get_text(strip=True)
                product_link = each.get('href', None)
                print(product, product_link)
                if product_link:
                    temp = {"product": product, "product_link": "https://ccpparts.com" + product_link}
                    data_product.append(temp)
        for index, each in enumerate(data_product):
            url2 = each['product_link']
            print(url2)
            try:
                r1 = requests.get(url2, headers=self.HEADERS)
                soup1 = BeautifulSoup(r1.text, 'html.parser')
                script_tag = soup1.find('script', text=re.compile(r'var meta'))
                javascript_code = script_tag.string
                pattern = r'\b{}\b\s*=\s*(.*?);'.format("var meta")
                match = re.search(pattern, javascript_code)
                if match:
                    variable_contents = match.group(1)
                    data = json.loads(variable_contents)
                    data_lst = data.get('products', None)
                    if data_lst:
                        each['subitems'] = []
                        for sub in data_lst:
                            sub_product = sub['variants'][0]['name']
                            price = sub['variants'][0]['price'] / 100
                            each['subitems'].append({'sub_product': sub_product, 'price': price})
                            print(each)
                        if index % 10 == 0:
                            time.sleep(10)
            except Exception as e:
                print(e)

        for each in data_product:
            for sub in each.get('subitems', []):
                temp = {}
                if each['product'] == "All Device":
                    temp['product_title'] = ""
                else:
                    temp['product_title'] = each['product'].lower()
                temp['name'] = sub['sub_product'].replace("For", "").strip()
                temp['price'] = sub['price']
                frame.append(temp)

        df = pd.DataFrame(frame)
        df.to_csv('base_product_2.csv',index=False)
        return frame

