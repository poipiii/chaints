import uuid #used for product id in product_model

#user account details
#user model - email,username,password,orders,payment,address
#orders - item,price,quantity, order id
class User_Model:
    #initaliser of User_Model 
    def __init__(self,user_email,username,user_password,user_firstname,user_lastname):
        self.__user_email=user_email
        self.__username=username
        self.__user_password=hash(user_password)
        self.__user_firstname=user_firstname
        self.__user_lastname=user_lastname

    #User_Model Mutator
    def set_user_email(self,user_email):
        self.__user_email=user_email

    def set_username(self,username):
        self.__username=username

    def set_user_password(self,user_password):
        self.__user_password=hash(user_password)

    def set_user_firstname(self,user_firstname):
        self.__user_firstname=user_firstname

    def set__user_lastname(self,user_lastname):
        self.__user_lastname=user_lastname

    #User_Model Accessor
    def get_user_email(self):
        return self.__user_email

    def get_username(self):
        return self.__username

    def get_user_password(self):
        return self.__user_password

    def get_user_firstname(self):
        return self.__user_firstname

    def get_user_lastname(self):
        return self.__user_lastname

    def get_user_fullname(self):
        return self.__user_firstname+" "+self.__user_lastname





class Product_Model:
    def __init__(self,product_name,product_current_qty,product_desc,product_price,product_discount):
        #initaliser of Product_Model
        self.__product_id = uuid.uuid4().hex #genterates a 32 bit random hexadecimal string that will be the product id
        self.__product_name =product_name
        self.__product_current_qty = product_current_qty
        self.__product_sold_qty = 0
        self.__product_desc = product_desc
        self.__product_price = product_price
        self.__product_discount = product_discount
        self.__product_images = {}
        self.__product_catergory = [] 
        
    #Product_Model Mutator 
    def set_product_id(self):
        self.__product_id = uuid.uuid4().hex #used for genterating another id if it exist in shelve

    def set_product_name(self,product_name):
        self.__product_name = product_name

    def set_product_current_qty(self,product_current_qty):
        self.__product_current_qty = product_current_qty

    def set_product_sold_qty(self,product_sold_qty):
        self.__product_sold_qty = product_sold_qty

    def set_product_desc(self,product_desc):
        self.__product_desc = product_desc

    def set_product_price(self,product_price):
        self.__product_price =product_price

    def set_product_discount(self,product_discount):
        self.__product_discount = product_discount
    def set_product_images(self,product_images):
        self.__product_images =product_images

    def set_product_catergory(self,product_catergory):
        self.__product_catergory = product_catergory

    #Product_Model Accessor 
    def get_product_id(self):
        return self.__product_id

    def get_product_name(self):
        return self.__product_name

    def get_product_current_qty(self):
        return self.__product_current_qty

    def get_product_sold_qty(self):
        return self.__product_sold_qty

    def get_product_desc(self):
        return self.__product_desc

    def get_product_price(self):
        return self.__product_price

    def get_product_discount(self):
        return self.__product_discount

    def get_product_images(self):
        return self.__product_images

    def get_product_catergory(self):
        return self.__product_catergory