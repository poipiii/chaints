import uuid #used for product id in product_model
import shelve
from datetime import datetime
from passlib.hash import pbkdf2_sha256
#user account details
#user model - email,username,password,orders,payment,address
#orders - item,price,quantity, order id
class User_Model:
    #initaliser of User_Model
    def __init__(self,user_email,username,user_password,user_firstname,user_lastname,user_role,joined_date):
        self.__user_role=user_role
        self.__user_id = uuid.uuid4().hex
        self.__user_email=user_email
        self.__username=username
        self.__user_password=pbkdf2_sha256.hash(user_password)
        self.__user_firstname=user_firstname
        self.__user_lastname=user_lastname
        self.set_owned_products()
        self.__user_wishlist=[]
        self.__user_joined_date=joined_date


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

    def set_owned_products(self):
        if self.__user_role == 'A':
            self.__owned_products = []
        else:
            self.__owned_products = None
    def append_owned_p(self,productid):
        self.__owned_products.append(productid)

    def delete_owned_p(self,productid):
        self.__owned_products.remove(productid)

    def set_user_wishlist(self,wishlist):
        self.__user_wishlist=wishlist

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

    def get_owned_products(self):
        return self.__owned_products

    def get_user_wishlist(self):
        return self.__user_wishlist

    def get_user_joined_date(self):
        return self.__user_joined_date



    def __str__(self):
        return 'username: {} email: {} password:{} firstname:{} lastname:{} fullname:{} usr_id:{} usr_role:{} owned_p:{}'.format(self.get_username(),self.get_user_email(),self.get_user_password(),self.get_user_firstname(),self.get_user_lastname(),self.get_user_fullname()
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
        discounted_price = self.get_product_price() - self.get_product_discount()
        return discounted_price
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


#product db test codes
#print all products in product db in command line
# def test_print():
#     db = shelve.open('database/product_database/product.db','c')
#     for i in db.values():
#         print(i)

#     db.close()

# test_print()
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
    def set_user_log_list(self,log_obj):
        self.__user_log_list.append(log_obj)
    def set_product_log_list(self,log_obj):
        self.__product_log_list.append(log_obj)
    def set_order_log_list(self,log_obj):
        self.__order_log_list.append(log_obj)
    def get_log_user_id(self):
        return self.__log_user_id
    def get_user_log_list(self):
        return self.__user_log_list
    def get_product_log_list(self):
        return self.__product_log_list
    def get_order_log_list(self):
        return self.__order_log_list


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
       
class orders_logger:
    def __init__(self,o_amount,product_id,order_obj):
        self.__o_amount = o_amount
        self.set_o_profit(o_amount,product_id)
        self.__timestamp = datetime.timestamp(datetime.now())
        self.__product_id = product_id
        self.__order_obj = order_obj
    def set_o_profit(self,o_amount,product_id):
        self.__o_profit = float(o_amount) * float(get_product_by_id(product_id).get_product_price())
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
    all_logs = db.get(user_id)
    product_logs = all_logs.get_product_log_list() 
    db.close()
    return product_logs

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
    def __init__(self,prodid,quantity,orderdate,sellerid,productname,productimage,buyerid): #
        self.__productid=prodid
        self.__sellerid=sellerid
        self.__quantity=quantity
        self.__deliverystat="Pending"
        self.__order_date=orderdate
        self.__indi_orderid= uuid.uuid4().hex
        self.__product_name=productname
        self.__product_image=productimage
        self.__delivery_location="Pending"
        self.__buyerid=buyerid

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
    def get_product_name(self):
        return self.__product_name
    def get_product_image(self):
        return self.__product_image
    def get_delivery_location(self):
        return self.__delivery_location
    def get_buyer_id(self):
        return self.__buyerid


def obtaining_product_object(product_id):
    product_obj=get_product_by_id(product_id)
    return product_obj

##separating the orders in the order so that each item will have their own separate order id
##{'someid':3}

def separating_orders(customerid,userorders,orderdate): #reminder: ADDRESS ALSO TO BE PASSED IN FROM ORDER
    productinfo={}
    for n in userorders:
        prod_iddict={}
        productobject=obtaining_product_object(n)
        sellerid=productobject.get_seller_id()
        productname=productobject.get_product_name()
        productimage=productobject.get_product_images()
        productimage=productimage[0]
        prod_iddict["Product Name"]=productname
        prod_iddict["Product Image"]=productimage
        prod_iddict["Seller ID"]=sellerid
        productinfo[n]=prod_iddict
    somelist=[]
    for i in userorders:  #{'123shirt':3,'124pants':5,'125shoe':6}
        indiproduct=indi_product_order(i,userorders[i],orderdate,productinfo[i]["Seller ID"],productinfo[i]["Product Name"],productinfo[i]["Product Image"],customerid)#
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




def print_db_orders():
    db=shelve.open('database/delivery_database/delivery.db','r')
    count=0
    for i in db:
        #print("customer id: %s"%i)
        count+=1
        for n in db[i]:
            print("customer id: %s"%n.get_buyer_id())
            print("Seller id: %s"%n.get_seller_id())
            print("Product id: %s"%n.get_product_id())
            print("Prduct Name: %s"%n.get_product_name())
            print("Quantity: %d"%n.get_quantity())
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

    #db.close()

#print_db_seller("16d1083a5963449d84d4ce0ae2088752")
#print_db_seller("cfeae366add04e69b6ff51974f6bbe9f")
#====clear delivery db======
#db=shelve.open('database/delivery_database/delivery.db','c')
#print(db.get)
#del db["345buy"]
#del db["678buy"]
#print(db)
#db.close()

#=====test (delivery)========

#o1dict={"4ab7e5c164b24502bfccd49fec034e41":3}
#o2dict={"4ab7e5c164b24502bfccd49fec034e41":6,"f9c18482274d42b8a2abd405698003ff":7}
#o3dict={"de79a6cc861f48788e586cc44287f7d7":2}
#o4dict={"29bc204ed2c0467597c227dcb3d914f6":3}
#o5dict={"29bc204ed2c0467597c227dcb3d914f6":3,"4ab7e5c164b24502bfccd49fec034e41":5}
#o1=separating_orders("678buy",o1dict,"12/12/2002")
#o2=separating_orders("345buy",o2dict,"13/12/2002")
#o3=separating_orders("999buy",o3dict,"14/12/2002")
#o5=separating_orders("112buy",o5dict,"5/1/2020")

#print_db_orders()
#
#status_update("4ab7e5c164b24502bfccd49fec034e41","678buy","Transit")
#
#print_db_orders()








