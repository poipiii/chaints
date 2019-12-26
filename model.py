import uuid #used for product id in product_model
import shelve
from datetime import datetime
from passlib.hash import pbkdf2_sha256
#user account details
#user model - email,username,password,orders,payment,address
#orders - item,price,quantity, order id
class User_Model:
    #initaliser of User_Model 
    def __init__(self,user_email,username,user_password,user_firstname,user_lastname,user_role):
        self.__user_role=user_role
        self.__user_id = uuid.uuid4().hex
        self.__user_email=user_email
        self.__username=username
        self.__user_password=pbkdf2_sha256.hash(user_password)
        self.__user_firstname=user_firstname
        self.__user_lastname=user_lastname

    #User_Model Mutator
    def set_user_role(self,user_role):
        self.__user_role=user_role

    def set_user_id(self):
        self.__user_id=uuid.uuid4().hex

    def set_user_email(self,user_email):
        self.__user_email=user_email

    def set_username(self,username):
        self.__username=username

    def set_user_password(self,user_password):
        self.__user_password=user_password

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

    def get_user_id(self):
        return self.__user_id

    def get_user_role(self):
        return self.__user_role





class Product_Model:
    def __init__(self,product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
        #initaliser of Product_Model
        self.__product_id = uuid.uuid4().hex #genterates a 32 bit random hexadecimal string that will be the product id
        self.__product_name =product_name
        self.__product_current_qty = product_current_qty
        self.__product_sold_qty = 0
        self.__product_desc = product_desc
        self.__product_price = product_price
        self.__product_discount = product_discount
        self.__product_images = product_images
        self.__product_catergory = product_catergory
        
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
    def get_discounted_price(self):
        discounted_price = self.get_product_price() - self.get_product_discount()
        return discounted_price
    def __str__(self):
        return 'name:{} uuid:{} current_qty:{} sold_qty:{} desc:{} price:{} discount:{} img:{} catergory:{}'.format(self.get_product_name(),self.get_product_id(),str(self.get_product_current_qty())
        ,str(self.get_product_sold_qty()),self.get_product_desc(),str(self.get_product_price()),str(self.get_product_discount()),self.get_product_images(),self.get_product_catergory())




#take in product form fields and creaste new product and put into db
def Add_New_Products(product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
    try:
        db = shelve.open('database/product_database/product.db','c')
        New_Product = Product_Model(product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images)       
        db[New_Product.get_product_id()] = New_Product

    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()


#grab all products in product db and return it
def fetch_products():
    try:
        product_list = []
        db = shelve.open('database/product_database/product.db','r')
        for i in db.values():
            product_list.append(i)
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()
    return product_list

#take in product id and return the specific product details 
def get_product_by_id(product_id):
    try:
       
        db = shelve.open('database/product_database/product.db','r')      
        product = db.get(product_id)
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()
    return product


#edit take in product id and all product fields and overwrite sand update product in db 
def Edit_Products(product_id,product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
    try:
        db = shelve.open('database/product_database/product.db','w')
        if product_id in db.keys():
            edit_product = db.get(product_id)
            edit_product.set_product_name(product_name)
            edit_product.set_product_current_qty(product_current_qty)
            edit_product.set_product_desc(product_desc)
            edit_product.set_product_price(product_price)
            edit_product.set_product_discount(product_discount)
            edit_product.set_product_catergory(product_catergory)
            edit_product.set_product_images(product_images)
            db[edit_product.get_product_id()] = edit_product
        else:
            print('error product not found ')
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()


#take in product id and delete product in db
def delete_product_by_id(product_id):
    try:
       
        db = shelve.open('database/product_database/product.db','r')    
        del(db[product_id])  
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()



#product db test codes 
#print all products in product db in command line
# def test_print():
#     db = shelve.open('database/product_database/product.db','c')  
#     x = 0
#     for i in db.values():
#         print(i)
#         x+=1        
#     print(len(db))
#     print(x)
#     db.close() 


#USE WITH CAUTION DELETE THE WHOLE PRODUCT DB
# def delete_db():
#     db = shelve.open('database/product_database/product.db','c') 
#     db.clear() 
#     db.close() 

#USE WITH CAUTION CREATE 30 GREY SHIRT PRODUCT IN PRODUCT DB


# for i in range(29):
#     Add_New_Products('grey shirt',200,'very grey shirt',100,1,['male'],['mango-man-1156-4297221-1.jpg'])
#do not touch 
# def Add_New_Products(product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
#     try:
#         db = shelve.open('database/product_database/product.db','c')
#         New_Product = Product_Model(product_name,product_current_qty,product_desc,product_price,product_discount)
#         if New_Product.get_product_id() in db.keys():
#             New_Product.set_product_id()
#             New_Product = Product_Model(product_name,product_current_qty,product_desc,product_price,product_discount)
#             New_Product.set_product_catergory(product_catergory)
#             New_Product.set_product_images(product_images)
#             db[New_Product.get_product_id()] = New_Product

#         else:
#             New_Product = Product_Model(product_name,product_current_qty,product_desc,product_price,product_discount)
#             New_Product.set_product_catergory(product_catergory)
#             New_Product.set_product_images(product_images)
#             db[New_Product.get_product_id()] = New_Product
    
#     except KeyError:
#         raise ' key error in shelve'
    
#     db.close()


#model for activity logging
class Logger:
    def __init__(self,log_user_id):
        self.__log_user_id = log_user_id
        self.__product_log_list = []
        self.__user_log_list = []
        self.__order_log_list = []
        self.__delivery_log_list = []
    def set_product_log_list(self,log_obj):
        self.__product_log_list.append(log_obj)
    def get_log_user_id(self):
        return self.__log_user_id
    def get_product_log_list(self):
        return self.__product_log_list

class product_logger:
    def __init__(self,p_activity,product_id,product_obj):
        self.set_p_activty(p_activity)
        self.__timestamp = datetime.timestamp(datetime.now())
        self.__product_id = product_id
        self.__product_obj = product_obj
    def set_p_activty(self,p_activity):
        if p_activity == 'CREATE':
            self.__p_activity = 'Created a product'
        elif p_activity == 'DELETE':
            self.__p_activity = 'Deleted a product'
        elif p_activity == 'EDIT':
            self.__p_activity = 'Editied a product'
    def get_p_activity(self):
        return self.__p_activity
    def get_product_id(self):
        return self.__product_id
    def get_object(self):
        return self.__product_obj
    def get_timestamp(self):
        return self.__timestamp
    def get_timestamp_as_datetime(self):
        return datetime.fromtimestamp(self.__timestamp)
    def __str__(self):
        return 'activity: {},productid: {}, product_obj {},timestamp {},datetime {}'.format(self.get_p_activity(),self.get_product_id(),self.get_object(),self.get_timestamp(),self.get_timestamp_as_datetime())
       

def product_logging(userid,product_activity,product_id,product_obj):
    db = shelve.open('database/logs_database/logs.db','c')
    if userid in db:
        new_log = product_logger(product_activity,product_id,product_obj)
        product_log = db.get(userid)
        product_log.set_product_log_list(new_log)
        db[product_log.get_log_user_id()] = product_log
    else:
        user_new_logger = Logger(userid)
        new_log = product_logger(product_activity,product_id,product_obj)
        user_new_logger.set_product_log_list(new_log)
        db[user_new_logger.get_log_user_id()] = user_new_logger
        print('success2')
    db.close()

        

def print_log():
    db = shelve.open('database/logs_database/logs.db','c')
    test = db.get('TEST')
    for i in test.get_product_log_list():
        print(i)
    db.close()
print_log()

# test = product_logging('TEST','DELETE','123456789','TEST2')


# def delete_db():
#     db = shelve.open('database/logs_database/logs.db','c') 
#     db.clear() 
#     db.close() 
# delete_db()
# sheldict ={'1234uuid': {'user_log': ['TEST']}}
# log_list = []
# test_obj = "TEST"
# log_list.append(test_obj)
# test_dic = {} 
# test_dic['product_log'] = log_list
# sheldict['1234uuid'] = test_dic

# # test = sheldict.get('1234uuid')
# # test['product_log'].append('TEST3')
# # sheldict['1234uuid'] = test
# print(sheldict)


