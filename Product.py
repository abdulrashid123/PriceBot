from thefuzz import fuzz
from BaseSite import Base


class Product:


    @classmethod
    def get_similarity(cls,product1,product2):
        p1 = Base.remove_words_in_brackets(product1).lower()
        p2 = Base.remove_words_in_brackets(product2).lower()
        # embeddings = cls.MODEL.encode([p1, p2])
        similarity_score =fuzz.token_set_ratio(p1,p2)
        # print(similarity_score)
        # Define a similarity threshold (you can adjust this as needed)
        similarity_threshold = 0.85

        # Determine if the products have similar meanings based on the similarity score
        if similarity_score >= similarity_threshold:
            return True
        else:
            return False

    @classmethod
    def get_product_related(cls,product_lst,name,price):
        scores = []
        for product in product_lst:
            bucks = product.get('price',None)
            similarity = cls.get_similarity(name, product['name'])
            if similarity and bucks and abs(price-float(bucks)) < (price*0.2):
                scores.append({'name':product['name'],'price':float(bucks)})
        return scores

# p3 = "Samsung Galaxy J3 Pro OLED Screen Assembly Replacement Without Frame "
# product1 = "iPhone 13 Pro Max OLED Screen Replacement"
# product2 = "iPhone 14 Pro Max OLED Screen Assembly Replacement"
# print(Product.get_similarity(product1,product2))