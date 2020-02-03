import uuid #used for product id in product_model
import shelve
from datetime import datetime,timedelta
from passlib.hash import pbkdf2_sha256
import random
#user account details
#user model - email,username,password,orders,payment,address
#orders - item,price,quantity, order id
class User_Model:
    #initaliser of User_Model
    def __init__(self,user_email,username,user_pw,user_firstname,user_lastname,role,joined_date):
        self.__user_id = uuid.uuid4().hex
        self.__user_email=user_email
        self.__username=username
        self.__user_pw=pbkdf2_sha256.hash(user_pw)
        self.__user_firstname=user_firstname
        self.__user_lastname=user_lastname
        self.__user_role=role
        self.set_owned_products()
        self.__user_wishlist=[]
        self.__user_joined_date=joined_date
        self.__user_address={}
        self.__user_profile_picture='http://s3.amazonaws.com/37assets/svn/765-default-avatar.png'


    #User_Model Mutator
    def set_user_role(self,user_role):
        self.__user_role=user_role

    def set_user_id(self):
        self.__user_id=uuid.uuid4().hex

    def set_user_email(self,user_email):
        self.__user_email=user_email

    def set_username(self,username):
        self.__username=username

    def set_user_pw(self,user_pw):
        self.__user_pw=pbkdf2_sha256.hash(user_pw)

    def set_user_firstname(self,user_firstname):
        self.__user_firstname=user_firstname

    def set_user_lastname(self,user_lastname):
        self.__user_lastname=user_lastname

    def set_owned_products(self):
        if self.__user_role == 'S':
            self.__owned_products = []
        else:
            self.__owned_products = None
    def append_owned_p(self,productid):
        self.__owned_products.append(productid)

    def delete_owned_p(self,productid):
        self.__owned_products.remove(productid)

    def set_user_wishlist(self,wishlist):
        self.__user_wishlist=wishlist

    def set_user_address(self,address):
        self.__user_address=address

    def set_user_profile_picture(self,profile_picture):
        self.__user_profile_picture=profile_picture

    #User_Model Accessor
    def get_user_email(self):
        return self.__user_email

    def get_username(self):
        return self.__username

    def get_user_pw(self):
        return self.__user_pw

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

    def get_owned_products(self):
        return self.__owned_products

    def get_user_wishlist(self):
        return self.__user_wishlist

    def get_user_joined_date(self):
        return self.__user_joined_date

    def get_user_address(self):
        return self.__user_address

    def get_user_profile_picture(self):
        return self.__user_profile_picture


    def __str__(self):
        return 'username: {} email: {} password:{} firstname:{} lastname:{} fullname:{} usr_id:{} usr_role:{} owned_p:{}'.format(self.get_username(),self.get_user_email(),self.get_user_pw(),self.get_user_firstname(),self.get_user_lastname(),self.get_user_fullname()
        ,self.get_user_id(),self.get_user_role(),self.get_owned_products())


def update_usr_owned_p(userid,productid):
    db = shelve.open('database/user_database/user.db','w')
    if userid in db:
        user = db.get(userid)
        user.append_owned_p(productid)
        db[userid] = user
    else:
        pass
    db.close()

def get_usr_owned_p(userid):
    db = shelve.open('database/user_database/user.db','r')
    if userid in db:
        user = db.get(userid)
        ownp = user.get_owned_products()
    else:
        pass
    return ownp
    db.close()

def get_user(userid):
    db = shelve.open('database/user_database/user.db','r')
    if userid in db.keys():
        user = db.get(userid)
        db.close()
    return user

def update_user(user_obj):
    db = shelve.open('database/user_database/user.db','r')
    if user_obj.get_user_id() in db.keys():
        db[user_obj.get_user_id()] = user_obj
        db.close()


# def delete_db():
#     db = shelve.open('database/user_database/user.db','c')
#     db.clear()
#     db.close()



# test_usr = User_Model('qq@qmail.com','poipii','654321','P','I','B')
# print(test_usr)

# def print_user_db():
#     db = shelve.open('database/user_database/user.db','r')
#     #for i in db.values():
#     print(db.get('dc588c5abbe24bf68d47dd556d1c6955'))
#     db.close()
# print_user_db()


class Product_Model:
    def __init__(self,seller_id,product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
        #initaliser of Product_Model
        self.__seller_id = seller_id
        self.__product_id = uuid.uuid4().hex #genterates a 32 bit random hexadecimal string that will be the product id
        self.__product_name =product_name
        self.__product_current_qty = product_current_qty
        self.__product_sold_qty = 0
        self.__product_desc = product_desc
        self.__product_price = product_price
        self.__product_discount = product_discount
        self.__product_images = product_images
        self.__product_catergory = product_catergory
        self.__product_reviews = []

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
    def set_product_reviews(self,reviews):
        self.__product_reviews.append(reviews)
    #Product_Model Accessor
    def get_seller_id(self):
        return self.__seller_id
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
        discounted_price = round(self.get_product_price() - self.get_product_discount(),2) 
        return discounted_price
    def get_product_reviews(self):
        return self.__product_reviews
    def __str__(self):
        return 'name:{} uuid:{} current_qty:{} sold_qty:{} desc:{} price:{} discount:{} img:{} catergory:{}'.format(self.get_product_name(),self.get_product_id(),str(self.get_product_current_qty())
        ,str(self.get_product_sold_qty()),self.get_product_desc(),str(self.get_product_price()),str(self.get_product_discount()),self.get_product_images(),self.get_product_catergory())






#take in product form fields and creaste new product and put into db
def Add_New_Products(user_id,product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
    try:
        db = shelve.open('database/product_database/product.db','c')
        New_Product = Product_Model(user_id,product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images)
        db[New_Product.get_product_id()] = New_Product
        update_usr_owned_p(user_id,New_Product.get_product_id())
        product_logging(user_id,'CREATE',New_Product.get_product_id(),New_Product)

    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'


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
    
    db.close()
    return product_list


def fetch_products_by_user(user_id):
    try:
        user_products = []
        db = shelve.open('database/user_database/user.db','r')
        user = db.get(user_id)
        user_products = user.get_owned_products()
        db.close()
        product_list = []
        db = shelve.open('database/product_database/product.db','r')
        for i in user_products:
            product_list.append(db.get(i))
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'

    db.close()
    return product_list

#take in product id and return the specific product object
def get_product_by_id(product_id):
    try:

        db = shelve.open('database/product_database/product.db','r')
        if product_id in db:
            product = db.get(product_id)
        else:
            raise 'product id does not exist in database'
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()
    return product


#edit take in product id and all product fields and overwrite sand update product in db
def Edit_Products(user_id,product_id,product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
    try:
        user = get_user(user_id)
        db = shelve.open('database/product_database/product.db','w')
        if product_id in db.keys() and product_id in user.get_owned_products():
            edit_product = db.get(product_id)
            edit_product.set_product_name(product_name)
            edit_product.set_product_current_qty(product_current_qty)
            edit_product.set_product_desc(product_desc)
            edit_product.set_product_price(product_price)
            edit_product.set_product_discount(product_discount)
            edit_product.set_product_catergory(product_catergory)
            edit_product.set_product_images(product_images)
            db[product_id] = edit_product
            product_logging(user_id,'EDIT',product_id,edit_product)
        else:
            print('error product not found ')
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()


def updatequantity(user_id,product_id,quantity):
    user = get_user(user_id)
    try:
        db = shelve.open('database/product_database/product.db','w')
        if product_id in db.keys() and product_id in user.get_owned_products():
            updateqty = db.get(product_id)
            updateqty.set_product_current_qty(quantity)
            db[product_id] =updateqty
            product_logging(user_id,'EDIT',product_id,updateqty)
    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()
#take in product id and delete product in db
def delete_product_by_id(product_id,user_id):
    user = get_user(user_id)
    try:
        db = shelve.open('database/product_database/product.db','r')
        if product_id in db.keys() and product_id in user.get_owned_products():
            deleted_product = db.pop(product_id)
            user.delete_owned_p(product_id)
            update_user(user)
            product_logging(user_id,'DELETE',product_id,deleted_product)

    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()

def delete_all_user_product(product_id_list,user_id):
    user = get_user(user_id)
    try:
        db = shelve.open('database/product_database/product.db','r')
        for product_id in product_id_list:
            if product_id in db.keys() and product_id in user.get_owned_products():
                deleted_product = db.pop(product_id)
                user.delete_owned_p(product_id)
                update_user(user)
                product_logging(user_id,'DELETE',product_id,deleted_product)

    except IOError:
        raise 'db file not found'
    except KeyError:
        raise ' key error in shelve'
    except:
        raise 'unknown error'
    db.close()


def add_review(userid,username,productid,rating,review_txt):
    review_dict = {'userid':userid,'username':username,'rating':rating,'review_txt':review_txt}
    db = shelve.open('database/product_database/product.db','w')
    if productid in db:
        product = db.get(productid)
        product.set_product_reviews(review_dict)
        db[productid] = product
    print(review_dict)
    db.close()



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
        self.__faq_log_list=[]
    def set_user_log_list(self,log_obj):
        self.__user_log_list.append(log_obj)
    def set_product_log_list(self,log_obj):
        self.__product_log_list.append(log_obj)
    def set_order_log_list(self,log_obj):
        self.__order_log_list.append(log_obj)
    def set_faq_log_list(self,log_obj):
        self.__faq_log_list.append(log_obj) 
    def get_log_user_id(self):
        return self.__log_user_id
    def get_user_log_list(self):
        return self.__user_log_list
    def get_product_log_list(self):
        return self.__product_log_list
    def get_order_log_list(self):
        return self.__order_log_list
    def get_faq_log_list(self):
        return self.__faq_log_list

class user_logger:
    def __init__(self,u_activity,user_id,user_obj):
        self.set_u_activty(u_activity)
        self.__timestamp = datetime.timestamp(datetime.now())
        self.__user_id = user_id
        self.__user_obj = user_obj
    def set_u_activty(self,u_activity):
        if u_activity == 'CREATE':
            self.__u_activity = 'User signed up'
        elif u_activity == 'DELETE':
            self.__u_activity = 'User deleted'
        elif u_activity == 'EDIT':
            self.__u_activity = 'User infomation edited'
        elif u_activity == 'LOGIN':
            self.__u_activity = 'User login'
        elif u_activity == 'LOGOUT':
            self.__u_activity = 'User logout'     
    def get_u_activity(self):
        return self.__u_activity
    def get_user_id(self):
        return self.__user_id
    def get_object(self):
        return self.__user_obj
    def get_timestamp(self):
        return self.__timestamp
    def get_timestamp_as_datetime(self):
        return datetime.fromtimestamp(self.__timestamp)
    def __str__(self):
        return 'activity: {},productid: {}, product_obj {},timestamp {},datetime {}'.format(self.get_u_activity(),self.get_user_id(),self.get_object(),self.get_timestamp(),self.get_timestamp_as_datetime())
       

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
        return 'activity: {} ,userid: {}, user_obj {},timestamp {},datetime {}'.format(self.get_p_activity(),self.get_product_id(),self.get_object(),self.get_timestamp(),self.get_timestamp_as_datetime())
       

def current_week(p_year,p_week):
    mon = datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    mon = datetime.combine(mon,datetime.min.time())
    tues = datetime.combine(mon+timedelta(days=1),datetime.min.time())
    wed = datetime.combine(mon+timedelta(days=2),datetime.min.time()) 
    thurs = datetime.combine(mon+timedelta(days=3),datetime.min.time())
    fri =  datetime.combine(mon+timedelta(days=4),datetime.min.time())
    sat = datetime.combine(mon+timedelta(days=5),datetime.min.time())
    sun = datetime.combine(mon+timedelta(days=6),datetime.min.time())
    return [mon,tues,wed,thurs,fri,sat,sun]

class orders_logger:
    def __init__(self,o_amount,product_id,order_obj):
        self.__o_amount = o_amount
        self.set_o_profit(o_amount,product_id)
        # self.__timestamp = datetime.timestamp(datetime.now())
        self.__timestamp = datetime.timestamp(random.choice(current_week('2020','5')))
        self.__product_id = product_id
        self.set_ordered_product_name(product_id)
        self.__order_obj = order_obj
    def set_o_profit(self,o_amount,product_id):
        self.__o_profit = float(o_amount) * float(get_product_by_id(product_id).get_product_price())
    def set_ordered_product_name(self,product_id):
        self.__ordered_product_name = get_product_by_id(product_id).get_product_name()
    def get_o_amount(self):
        return self.__o_amount
    def get_o_profit(self):
        return self.__o_profit
    def get_product_id(self):
        return self.__product_id
    def get_object(self):
        return self.__order_obj
    def get_timestamp(self):
        return self.__timestamp
    def get_timestamp_as_datetime(self):
        return datetime.fromtimestamp(self.__timestamp)
    def __str__(self):
        return 'order amt: {},order profit{},productid: {}, product_obj {},timestamp {},datetime {}'.format(self.get_o_amount(),self.get_o_profit(),self.get_product_id(),self.get_object(),self.get_timestamp(),self.get_timestamp_as_datetime())
       
class faq_logger:
    def __init__(self,faq_type,faq_activity,faq_id,faq_object):
        self.__faq_type = faq_type
        self.set_faq_activty(faq_activity)
        self.__timestamp = datetime.timestamp(datetime.now())
        self.__faq_id = faq_id
        self.__faq_object = faq_object
    def set_faq_activty(self,faq_activity):
        if faq_activity == 'CREATE':
            self.__faq_activity = 'Created a faq entry'
        elif faq_activity == 'DELETE':
            self.__faq_activity = 'Deleted a faq entry'
        elif faq_activity == 'EDIT':
            self.__faq_activity = 'Edited a faq entry'
    def get_faq_id(self):
        return self.__faq_id
    def get_faq_activity(self):
        return self.__faq_activity
    def get_faq_type(self):
        return self.__faq_type
    def get_faq_object(self):
        return self.__faq_object
    def get_timestamp(self):
        return self.__timestamp
    def get_timestamp_as_datetime(self):
        return datetime.fromtimestamp(self.__timestamp)
    def __str__(self):
        return 'faq_type: {},faq_activity: {},faq_id: {}, faq_object {},timestamp {},datetime {}'.format(self.get_faq_type(),self.get_faq_activity(),self.get_faq_id(),self.get_faq_object(),self.get_timestamp(),self.get_timestamp_as_datetime())




def user_logging(userid,user_activity,user_obj):
    db = shelve.open('database/logs_database/logs.db','c')
    if userid in db:
        new_log = user_logger(user_activity,userid,user_obj)
        product_log = db.get(userid)
        product_log.set_user_log_list(new_log)
        db[userid] = product_log
    else:
        user_new_logger = Logger(userid)
        new_log = user_logger(user_activity,userid,user_obj)
        user_new_logger.set_product_log_list(new_log)
        db[userid] = user_new_logger
    db.close()

#take in user id , product activity product id product _obj
def product_logging(userid,product_activity,product_id,product_obj):
    db = shelve.open('database/logs_database/logs.db','c')
    if userid in db:
        new_log = product_logger(product_activity,product_id,product_obj)
        product_log = db.get(userid)
        product_log.set_product_log_list(new_log)
        db[userid] = product_log
    else:
        user_new_logger = Logger(userid)
        new_log = product_logger(product_activity,product_id,product_obj)
        user_new_logger.set_product_log_list(new_log)
        db[userid] = user_new_logger
    db.close()

def faq_logging(userid,faq_type,faq_activity,faq_id,faq_object):
    db = shelve.open('database/logs_database/logs.db','c')
    if userid in db:
        new_log = faq_logger(faq_type,faq_activity,faq_id,faq_object)
        faq_log = db.get(userid)
        faq_log.set_faq_log_list(new_log)
        db[userid] = faq_log
    else:
        user_new_logger = Logger(userid)
        new_log = faq_logger(faq_type,faq_activity,faq_id,faq_object)
        user_new_logger.set_faq_log_list(new_log)
        db[userid] = user_new_logger
    db.close()


def order_log_preprocess(userid,orderobj):
    user_order = orderobj.get_cart_list()
    for orders in user_order:
        order_logging(userid,user_order[orders],orders,orderobj)



def order_logging(userid,order_amt,product_id,order_obj):
    db = shelve.open('database/logs_database/logs.db','c')
    if userid in db:
        new_log = orders_logger(order_amt,product_id,order_obj)
        order_log = db.get(userid)
        order_log.set_order_log_list(new_log)
        db[userid] = order_log
    else:
        user_new_logger = Logger(userid)
        new_log = orders_logger(order_amt,product_id,order_obj)
        user_new_logger.set_order_log_list(new_log)
        db[userid] = user_new_logger
    db.close()


def get_user_log_by_id(user_id):
    db = shelve.open('database/logs_database/logs.db','r')
    all_logs = db.get(user_id)
    product_logs = all_logs.get_user_log_list() 
    db.close()
    return product_logs

def get_product_log_by_id(user_id):
    db = shelve.open('database/logs_database/logs.db','r')
    if user_id in db:
        all_logs = db.get(user_id)
        product_logs = all_logs.get_product_log_list() 
        return product_logs
    else:
        return None
    db.close()

def get_order_log_by_id(user_id):
    db = shelve.open('database/logs_database/logs.db','r')
    all_logs = db.get(user_id)
    order_logs = all_logs.get_order_log_list() 
    db.close()
    return order_logs



# def print_log():
#     db = shelve.open('database/logs_database/logs.db','r')
#     test = db.get('49aa66e5bf71407daa1c6e91f41cbdb6')
#     for i in test.get_order_log_list():
#         print(i)
#     db.close()
# print_log()



# test = user_logging('17187343a81c4de4aed19489cbe8a41a','DELETE','TEST2')

# def delete_db():
#     db = shelve.open('database/logs_database/logs.db','c') 
#     db.clear() 
#     db.close() 
# delete_db()

#delivery stuff

class indi_product_order:
    def __init__(self,prodid,quantity,orderdate,sellerid,productname,productimage,buyerid,address,sellername,buyername): #remember to get address from order,also need find way to get estimated order date
        self.__productid=prodid
        self.__sellerid=sellerid
        self.__sellername=sellername
        self.__quantity=quantity
        self.__deliverystat="Pending"
        self.__order_date=orderdate
        self.__indi_orderid= uuid.uuid4().hex
        self.__product_name=productname
        self.__product_image=productimage
        self.__delivery_location="Pending"
        self.__buyerid=buyerid
        self.__buyername=buyername
        self.__address=address

    #mutator
    def set_delivery_status(self,delivery_stat):
        self.__deliverystat=delivery_stat
    def set_delivery_location(self,location): #only carrier can edit
        self.__delivery_location=location

    #accessor
    def get_product_id(self):
        return self.__productid
    def get_quantity(self):
        return self.__quantity
    def get_deliverystat(self):
        return self.__deliverystat
    def get_order_date(self):
        return self.__order_date
    def get_individual_orderid(self):
        return self.__indi_orderid
    def get_seller_id(self):
        return self.__sellerid
    def get_seller_name(self):
        return self.__sellername
    def get_product_name(self):
        return self.__product_name
    def get_product_image(self):
        return self.__product_image
    def get_delivery_location(self):
        return self.__delivery_location
    def get_buyer_id(self):
        return self.__buyerid
    def get_buyer_name(self):
        return self.__buyername
    def get_address(self):
        return self.__address


#class to create individual tracking details for each delivery based on delivery status
class carrier_delivery:
    def __init__(self,statusdate,location,status,deliverynotes,address):
        self.__statusdate=statusdate
        self.__location=location
        self.__status=status
        self.__deliverynotes=deliverynotes
        self.__address=address

    #accessors
    def get_status_date(self):
        return self.__statusdate
    def get_status(self):
        return self.__status
    def get_location(self):
        return self.__location
    def get_delivery_notes(self):
        return self.__deliverynotes
    def get_address(self):
        return self.__address

#creates carrier updates object and stores in db
def carrierobj_and_db(orderid,statusdate,location,status,deliverynotes,address):
    carrierobj=carrier_delivery(statusdate,location,status,deliverynotes,address)
    db=shelve.open("database/delivery_database/carrier.db","c")
    if orderid in db:
        statuslist=db[orderid]
        statuslist.append(carrierobj)
        db[orderid]=statuslist
    else:
        statuslist=[]
        statuslist.append(carrierobj)
        db[orderid]=statuslist
    db.close()

def print_db():
    db=shelve.open("database/delivery_database/carrier.db","c")
    for i in db:
        print("Order id %s"%i)
        for n in db[i]:
            print("Status: %s"%n.get_status())
            print("Location: %s"%n.get_location())
            print("Notes: %s"%n.get_location())
    db.close()

#carrierobj_and_db("order1","12/12/12","Singapore","Transit","Slight delay","123 Happy")
#print_db()

def obtaining_product_object(product_id):
    product_obj=get_product_by_id(product_id)
    return product_obj

##separating the orders in the order so that each item will have their own separate order id
##{'someid':3}

def separating_orders(customerid,userorders,orderdate,address): #reminder: ADDRESS ALSO TO BE PASSED IN FROM ORDER
    productinfo={}
    for n in userorders:
        prod_iddict={}
        productobject=obtaining_product_object(n)
        sellerid=productobject.get_seller_id()
        productname=productobject.get_product_name()
        productimage=productobject.get_product_images()
        productimage=productimage[0]
        db=shelve.open('database/user_database/user.db','r')
        userobj=db[sellerid]
        sellername=userobj.get_username()
        db.close()
        prod_iddict["Product Name"]=productname
        prod_iddict["Product Image"]=productimage
        prod_iddict["Seller ID"]=sellerid
        prod_iddict["Seller Name"]=sellername
        productinfo[n]=prod_iddict
    buyerobj=obtaining_buyer_object(customerid)
    buyername=buyerobj.get_username()
    somelist=[]
    for i in userorders:  #{'123shirt':3,'124pants':5,'125shoe':6}
        indiproduct=indi_product_order(i,userorders[i],orderdate,productinfo[i]["Seller ID"],productinfo[i]["Product Name"],productinfo[i]["Product Image"],customerid,address,productinfo[i]["Seller Name"],buyername)#
        somelist.append(indiproduct)
    try:
        db = shelve.open('database/delivery_database/delivery.db','c')
        db[customerid]=somelist
        #db.clear()
        db.close()
    except IOError:
        raise Exception('db cannot be found')
    except:
        raise Exception("an unknown error has occurred ")


#get buyer object
def obtaining_buyer_object(customerid):
    try:
        db=shelve.open('database/user_database/user.db','r')
        buyerobj=db[customerid]
        db.close()
        return buyerobj
    except IOError:
        raise Exception('db not found')
    except:
        raise Exception('an error occurred')


#edit delivery status
def status_update(product_id,buyerid,status):
    try:
        db=shelve.open('database/delivery_database/delivery.db','c')
        a=db[buyerid]
        for i in a:
            if i.get_product_id()==product_id:
                i.set_delivery_status(status)
        db[buyerid]=a

        db.close()
    except IOError:
        raise Exception("db does not exist")
    except:
        raise Exception("an error has occurred")

#to get the necessary stuff in order to pass to status_update function
def passing_app_to_update(orderid,status):
    try:
        db=shelve.open('database/delivery_database/delivery.db','c')
        for i in db:
            for n in db[i]:
                if n.get_individual_orderid()==orderid:
                    status_update(n.get_product_id(),n.get_buyer_id(),status)
        db.close()
    except IOError:
        raise Exception("db does not exist")
    except:
        raise Exception("as error has occured")

    
#create buyer's order list
def create_buyer_order_list(buyerid):
    try:
        db=shelve.open('database/delivery_database/delivery.db','c')
        buyerorderlist=[]
        if buyerid in db:
            for i in db[buyerid]:
                buyerorderlist.append(i)
        db.close()
    except IOError:
        raise Exception("db does not exist")
    except:
        raise Exception("an error has occurred")
    return buyerorderlist

#to get products of seller
def obtaining_seller_product_id(sellerid):
    try:
        db=shelve.open('database/user_database/user.db','r')
        prod_id_list=[]
        seller=db.get(sellerid)
        prod_id_list=seller.get_owned_products() #gets list of product id of products owned by user
        db.close()
    except IOError:
        raise Exception("db not found")
    except:
        raise Exception("unknown error occurred")

    return prod_id_list

#to create list of objects for seller side
def create_seller_order_list(sellerid):
    try:
        db=shelve.open('database/delivery_database/delivery.db','r')
        seller_delivery_list=[]
        productidlist=obtaining_seller_product_id(sellerid)
        for i in productidlist: #running through product key list
            for n in db: #running through db, getting value from key n
                for j in db[n]: #running through list of obj (value of db[n])
                    if i==j.get_product_id():
                        seller_delivery_list.append(j)
        db.close()
        #db=shelve.open('database/delivery_seller_database/seller_del.db','c')
        #db[sellerid]=seller_delivery_list
        #db.close()
    except IOError:
        raise Exception("db does not exist")
    except:
        raise Exception("an unknown error has occurred")
    return seller_delivery_list

#to delete delivery object from delivery db and
def cancelling_carrier_side(orderid):
    try:
        statusobj=carrier_delivery("-","-","Delivery Cancelled","Cancelled by buyer","-")
        db=shelve.open('database/delivery_database/carrier.db','c')
        if orderid in db:
            statuslist=db[orderid]
        else:
            statuslist=[]
        statuslist.append(statusobj)
        db[orderid]=statuslist
        db.close()

    except IOError:
        raise Exception('db does not exist')
    except:
        raise Exception('an unknown error has occurred')

#cancelling order
def deleting_delivery(userid):
    try:
        db=shelve.open('database/delivery_database/delivery.db','r')
        del db[userid]
        db.close()
    except IOError:
        raise Exception('db does not exist')
    except:
        raise Exception('an unknown error has occurred')


def print_db_orders():
    db=shelve.open('database/delivery_database/delivery.db','r')
    count=0
    for i in db:
        #print("customer id: %s"%i)
        count+=1
        for n in db[i]:
            print("customer id: %s"%n.get_buyer_id())
            print("Customer name: %s"%n.get_buyer_name())
            print("Seller id: %s"%n.get_seller_id())
            print("Seller username: %s"%n.get_seller_name())
            print("Product id: %s"%n.get_product_id())
            print("Product Name: %s"%n.get_product_name())
            print("Quantity: %d"%n.get_quantity())
            print("Address: %s"%n.get_address())
            print("Order date: %s"%n.get_order_date())
            print("Order id: %s"%n.get_individual_orderid())
            print("Delivery status: %s"%n.get_deliverystat())
        print("============")
    print(count)
    print("===========")

def print_db_seller(sellerid):
    listy=create_seller_order_list(sellerid)
    print("Seller id: %s"%sellerid)
    print("========")
    for i in listy:
        print("customer id: %s"%i.get_buyer_id())
        print("Seller id: %s"%i.get_seller_id())
        print("Product id: %s"%i.get_product_id())
        print("Prduct Name: %s"%i.get_product_name())
        print("Quantity: %d"%i.get_quantity())
        print("Order date: %s"%i.get_order_date())
        print("Order id: %s"%i.get_individual_orderid())
        print("Delivery status: %s"%i.get_deliverystat())
        print("===^===^===")

def print_list_buyer(buyerid):
    listy=create_buyer_order_list(buyerid)
    print("Buyer id: %s"%buyerid)
    print("==========")
    for i in listy:
        print("Order id: %s"%i.get_individual_orderid())
        print("product id: %s"%i.get_product_id())
        print("seller id: %s"%i.get_seller_id())
        print("product name: %s"%i.get_product_name())
        print("Quantity: %s"%i.get_quantity())
        print("Order date: %s"%i.get_order_date())
        print("Delivery status: %s"%i.get_deliverystat())
    #db.close()

#print_db_seller("16d1083a5963449d84d4ce0ae2088752")
#print_db_seller("cfeae366add04e69b6ff51974f6bbe9f")
#====clear delivery db======
#db=shelve.open('database/delivery_database/delivery.db','c')
##print(db.get)
##del db["345buy"]
##del db["678buy"]
##print(db)
#db.clear()
#db.close()

#=====test (delivery)========
#o1dict={'65bed418f681479c95dc98b00b05923b':3,'8bc38fcbc4344b50bdce1f0a30793d57':2}
#o2dict={'523b6d50208b45f489b5a59ad67822a3':8,"a5eacc8a83144c4eb0cfcd36c4cea125":2}
###o3dict={'8bc38fcbc4344b50bdce1f0a30793d57':6}
###o1=separating_orders('8d11b80c18374832a116e6918b24a816',o1dict,'12/12/2012','123 sunny vale')
#o2=separating_orders('fb3047df8d6f41db97de800c5dbf81df',o2dict,'12/11/2012','456 greenwood ave')
##o3=separating_orders('123abd',o3dict,'12/11/2012','777 greenwood ave')

class Order:
    def __init__(self,cart_list,buyername,totalprice):
        self.__orderID=uuid.uuid4().hex
        self.__cart_list=cart_list
        self.__buyername=buyername
        self.__totalprice=totalprice
        # self.__sellerID=sellerID
        self.__timestamp = datetime.timestamp(datetime.now())
    def set_buyername(self,buyername):
        self.__buyername=buyername

    def set_totalprice(self,totalprice):
        self.__totalprice=totalprice

    # def set_sellerID(self,sellerID):
    #     self.__sellerID=sellerID

    def get_orderId(self):
        return self.__orderID

    def get_buyername(self):
        return self.__buyername

    def get_totalprice(self):
        return self.__totalprice

    def get_cart_list(self):
        return self.__cart_list

    # def get_sellerID(self):
    #     return self.__sellerID

    def get_timestamp(self):
        return self.__timestamp

    def get_timestamp_as_datetime(self):
        return datetime.fromtimestamp(self.__timestamp)

class confirm_order():
    def __init__(self,cardholder,cardno,expiry,cvc):
        self.__cardholder=cardholder
        self.__cardno=cardno
        self.__expiry=expiry
        self.__cvc=cvc
        self.__cartdict={}

    def set__cardholder(self,cardholder):
        self.__cardholder=cardholder

    def set__cardno(self,cardno):
        self.__cardno=cardno

    def set__expiry(self,expiry):
        self.__expiry=expiry

    def set__cvc(self,cvc):
        self.__cvc=cvc

    def set_cartdict(self,cartdict):
        self.__cartdict=cartdict

    def get_cardholder(self):
        return self.__cardholder

    def get_cardno(self):
        return self.__cardno

    def get_expiry(self):
        return self.__expiry

    def get_cvc(self):
        return self.__cvc

    def get_cartdict(self):
        return self.__cartdict

def delivery_info(DeliveryInfo):
    db=shelve.open('database/user_database/user.db','c')
    if session.get('user_id') in db:
        info=db.get(session.get('user_id'))
            #Infodict={}
            #Infodict["DeliveryInfo"]=info.get_deliveryinfo()
        db[session.get('user_id')]=info.get_user_address()
    db.close()

def add_delivery_info(address,country,city,state,zip,userid):
    add={}
    add["address"]=address
    add["country"]=country
    add["city"]=city
    add["state"]=state
    add["zip"]=zip
    db=shelve.open('database/user_database/user.db','c')
    if userid in db:
        a=db[userid]
        a.set_user_address(add)
        db[userid]=a
    else:
        db[userid]=add
    db.close()

def payment_confirmation(cardholder,cardno,expiry,cvc,userid):
    db=shelve.open('database/order_database/cart.db','c')# open the cart
    if userid in db:
        retrieve=db[userid]
    db.close()
    db=shelve.open('database/order_database/order.db','c')
    order_object=confirm_order(cardholder,cardno,expiry,cvc)
    db[userid]=order_object
    db.close()







class Dessage():
    def __init__(self,userid,mtitle,mbody):
        self.__userid=userid
        self.__mtitle=mtitle
        self.__mbody=mbody
    def getuid(self):
        return self.__userid
    def setmtitle(self,mtitle):
        self.__mtitle=mtitle
    def getmtitle(self):
        return self.__mtitle
    def setmbody(self,mbody):
        self.__mbody=mbody
    def getmbody(self):
        return self.__mbody
#Question
class CQuestion(Dessage):
    def __init__(self,UserID,mtitle,mbody):
        super().__init__(UserID,mtitle,mbody)
        self.__msgid_Qns=uuid.uuid4().hex
        self.__answers_list=[]
    def setanslist(self,ansid):
        self.__answers_list.append(ansid)
    def get_msgid(self):
        return self.__msgid_Qns
    def get_ans_list(self):
        return self.__answers_list
#Response
class CAnswer(Dessage):
    def __init__(self,UserID,mtitle,mbody):
        super().__init__(UserID,mtitle,mbody)
        mtitle=None        
        self.__ansid=uuid.uuid4().hex
        self.__Question=[]
    def setQuestion(self,Qnsid):
        self.__Question.append(Qnsid)
    def getQuestion(self):
        return self.__Question
    def get_ansid(self):
        return self.__ansid
#FAQ Forum Shelve DB

def get_question_by_id(question_id):
    db = shelve.open('database/forum_database/FAQQ.db','r')
    if question_id in db:
        question_obj = db.get(question_id)
        return question_obj
    else:
        print('question does not exist')
    db.close()


def RespondtoQns(Responseid, question_id):
    db = shelve.open('database/forum_database/FAQQ.db','c')
    if question_id in db:
        question_obj = db.get(question_id)
        question_obj.setanslist(Responseid)
        db[question_id]=question_obj
    else:
        print('question does not exist')
    db.close()


def get_answer_by_id(id):
    ans_obj_list = []
    db = shelve.open('database/forum_database/FAQQ.db','r')
    for i in id:
        if i in db:
            ans_obj = db.get(i)
            ans_obj_list.append(ans_obj)

        else:
                print('question does not exist')

    db.close()
    return ans_obj_list
class FAQQuestions():
    def __init__(self,question,answer):
        self.__faqid=uuid.uuid4().hex
        self.__question=question
        self.__answer=answer
    def setquestion(self,question):
        self.__question=question
    def getquestion(self):
        return self.__question
    def setanswer(self,answer):
        self.__answer=answer
    def getanswer(self):
        return self.__answer
    def getid(self):
        return self.__faqid
        
class FAQm(FAQQuestions):
    def __init__(self,question, answer):
        super().__init__(question,answer)
        
class Account_Issues(FAQQuestions):
    def __init__(self,question,answer):
        super().__init__(question,answer)
class Contact(FAQQuestions):
    def __init__(self,question,answer):
        super().__init__(question,answer)




#FAQ log display
# def retrive_all_faq_logs():
#     retrived_logs = []
#     faq_logs = []
#     db = shelve.open('database/logs_database/logs.db','r')
#     for user in db:
#         retrived_logs.append(db.get(user))
#     for user_logs in retrived_logs:
#         for faq_log in user_logs.get_faq_log_list():
#             faq_logs.append(faq_log)
#         db.close()
#     for i in faq_logs:
#         print(i)
# retrive_all_faq_logs()

#def test_faq_db():
#    Gold=[]
#    db = shelve.open('database/forum_database/FAQQ.db','r')
#    for i in db.values():
#        if isinstance(i,CQuestion):
#            Gold.append(i)
#    for i in Gold:
#        print (i.getmtitle(),i.getmbody())
#        print(i.get_msgid())
#test_faq_db()



#fr = shelve.open('database/forum_database/FAQQ.db','r')
#for i in fr:
#    if isinstance(i,CQuestion):
#        print(i.getmbody())
#fr.close()

#friend = shelve.open("database/forum_database/FAQDisplay.db",'r')
#a=friend.values()
#for aborginal in a:
#    print(aborginal.getquestion())
#friend.close()


#def test_faq_db():
#    db = shelve.open('database/forum_database/FAQQ.db','r')
#    for i in db.values():
#        if isinstance(i,CQuestion):
#           print (i.get_ans_list())
#        #elif isinstance(i,CAnswer):
#        else:
#            continue
#    db.close()
#test_faq_db()












