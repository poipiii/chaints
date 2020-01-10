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
        self.set_owned_products()
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
    

    
    def __str__(self):
        return 'username: {} email: {} password:{} firstname:{} lastname:{} fullname:{} usr_id:{} usr_role:{} owned_p:{}'.format(self.get_username(),self.get_user_email(),self.get_user_password(),self.get_user_firstname(),self.get_user_lastname(),self.get_user_fullname()
        ,self.get_user_id(),self.get_user_role(),self.get_owned_products())


def update_usr_owned_p(userid,productid):
    db = shelve.open('database/user_database/user.db','c') 
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
def Add_New_Products(user_id,product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images):
    try:
        db = shelve.open('database/product_database/product.db','c')
        New_Product = Product_Model(product_name,product_current_qty,product_desc,product_price,product_discount,product_catergory,product_images)       
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
    except:
        raise 'unknown error'
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
        print('success2')
    db.close()

        

# def print_log():
#     db = shelve.open('database/logs_database/logs.db','c')
#     test = db.get('b831c6bd18ef4d10bf625cacb443dcde')
#     for i in test.get_product_log_list():
#         print(i)
#     db.close()
# print_log()



#delivery stuff

#creating class for individual orders in one cart
class indi_product_order:
    def __init__(self,prodid,quantity):
        self.__productid=prodid
        self.__quantity=quantity
        self.__deliverystat="pending"
        self.__indi_orderid= uuid.uuid4().hex
    def get_product_id(self):
        return self.__productid
    def get_quantity(self):
        return self.__quantity
    def get_deliverystat(self):
        return self.__deliverystat

#separating the orders in the order so that each item will have their own separate order id
#sihui please use dictionary, have the product id be the key and the quantity be the value uwu
#{'someid':3}
def separating_orders(userid,userorders):
    sepdict={}
    somelist=[]
    for i in userorders:
        indiproduct=indi_product_order(i,userorders[i])
        somelist.append(indiproduct)
    sepdict[userid]=somelist #i put in dictionary first, still thinking whether to create a separate db for this
    return sepdict










# test = product_logging('TEST','DELETE','123456789','TEST2')


# def delete_db():
#     db = shelve.open('database/logs_database/logs.db','c') 
#     db.clear() 
#     db.close() 
# delete_db()

#FAQ Forum
class Message():
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
class CQuestion(Message):
    def __init__(self,UserID,mtitle,mbody):
        super().__init__(UserID,mtitle,mbody)
        self.__msgid_Qns=uuid.uuid4().hex
        self.__mtitle=mtitle
        self.__mbody=mbody
        self.__answers_list=[]
    def setanslist(self,ansid):
        self.__answers_list.append(ansid)
    def get_msgid(self):
        return self.__msgid_Qns
    def get_ans_list(self):
        return self.__answers_list
    #def __str__(self):
    #    return 'msgid:{},userid:{},mitle:{},mbody:{}'.format(self.get_msgid(),self.getuid(),self.getmtitle(),self.getmbody())
#Response
class CAnswer(Message):
    def __init__(self,UserID,mtitle,mbody):
        super().__init__(UserID,mtitle,mbody)
        mtitle=None        
        self.__mtitle=mtitle
        self.__mbody=mbody
        self.__ansid=uuid.uuid4().hex
        self.__Question=[]
    def setQuestion(self,Qnsid):
        self.__Question.append(Qnsid)
    def getQuestion(self):
        return self.__Question
    def get_ansid(self):
        return self.__ansid
    #def __str__(self):
    #    return 'msgid:{},userid:{},mitle:{},mbody:{}'.format(self.get_ansid(),self.getuid(),self.getmtitle(),self.getmbody())
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
    print(id)
    db = shelve.open('database/forum_database/FAQQ.db','r')
    for i in id:
        if i in db:
            ans_obj = db.get(i)
            ans_obj_list.append(ans_obj)

        else:
                print('question does not exist')
        
    db.close()
    return ans_obj_list



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



# db = shelve.open('database/forum_database/FAQQ.db','c')
# db.close()


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