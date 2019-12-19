import uuid #used for product id in product_model
import shelve
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
        self.__product_images = []
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
    def __str__(self):
        return 'name:{} uuid:{} current_qty:{} sold_qty:{} desc:{} price:{} discount:{} img:{} catergory:{}'.format(self.get_product_name(),self.get_product_id(),str(self.get_product_current_qty())
        ,str(self.get_product_sold_qty()),self.get_product_desc(),str(self.get_product_price()),str(self.get_product_discount()),self.get_product_images(),self.get_product_catergory())

def Add_New_Products(product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
    try:
        db = shelve.open('database/product_database/product.db','c')
        New_Product = Product_Model(product_name,product_current_qty,product_desc,product_price,product_discount)
        if New_Product.get_product_id() in db.keys():
            New_Product.set_product_id()
            New_Product = Product_Model(product_name,product_current_qty,product_desc,product_price,product_discount)
            New_Product.set_product_catergory(product_catergory)
            New_Product.set_product_images(product_images)
            db[New_Product.get_product_id()] = New_Product

        else:
            New_Product = Product_Model(product_name,product_current_qty,product_desc,product_price,product_discount)
            New_Product.set_product_catergory(product_catergory)
            New_Product.set_product_images(product_images)
            db[New_Product.get_product_id()] = New_Product
    
    except KeyError:
        raise ' key error in shelve'
    
    db.close()

# def fetch_products():
#     try:
#         product_list = []
#         db = shelve.open('database/product_database/product.db','c')
#         for i in db.values():
#             product_list.append(i)
#     except IOError:
#         raise 'db file not found'
#     except KeyError:
#         raise ' key error in shelve'
#     except:
#         raise 'unknown error'
#     db.close()

def test_print():
    try:
        product_list = []
        db = shelve.open('database/product_database/product.db','c')
        for i in db.values():
            product_list.append(i)
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close() 
    display_products(product_list)

def display_products(product_list):
    for i in product_list:
        print(i)       

test_print()