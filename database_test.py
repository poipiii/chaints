import shelve
from model import *
import os
import glob
import datetime
def dump_all():
    db = shelve.open('database/logs_database/logs.db','c')
    db.clear()
    db.close()
    db = shelve.open('database/product_database/product.db','c')
    db.clear()
    db.close()
    db = shelve.open('database/user_database/user.db','c')
    db.clear()
    db.close()
    db = shelve.open('database/delivery_database/delivery.db','c')
    db.clear()
    db.close()


def init_all():
    db = shelve.open('database/logs_database/logs.db','c')
    db.close()
    db = shelve.open('database/product_database/product.db','c')
    db.close()
    db = shelve.open('database/user_database/user.db','c')
    db.close()
    db = shelve.open('database/delivery_database/delivery.db','c')
    db.close()
    db = shelve.open('database/delivery_database/carrier.db','c')
    db.close()
    db = shelve.open('database/forum_database/FAQQ.db','c')
    db.close()
    db = shelve.open('database/order_database/cart.db','c')
    db.close()
    db = shelve.open('database/order_database/order.db','c')
    db.close()


def delete_all_db():
    files = glob.glob('database/user_database/*')
    for f in files:
        print(f)
        os.remove(f)
    files = glob.glob('database/product_database/*')
    for f in files:
        print(f)
        os.remove(f)
    files = glob.glob('database/order_database/*')
    for f in files:
        print(f)
        os.remove(f)
    files = glob.glob('database/delivery_database/*')
    for f in files:
       print(f)
       os.remove(f)
    files = glob.glob('database/forum_database/*')
    for f in files:
        print(f)
        os.remove(f)
    files = glob.glob('database/logs_database/*')
    for f in files:
        print(f)
        os.remove(f)    


init_all()
# for i in range(29):
#     Add_New_Products('grey shirt',200,'very grey shirt',100,1,['male'],['mango-man-1156-4297221-1.jpg'])



# db = shelve.open('database/user_database/user.db', 'w')
# user=User_Model('testadmin@testmail.com','testadmin','testadmin','test','admin','A',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# user=User_Model('testseller1@testmail.com','testseller1','testseller1','test','seller1','A',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# user=User_Model('testseller2@testmail.com','testseller2','testseller2','test','seller2','A',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# user=User_Model('testbuyer1@testmail.com','testbuyer1','testbuyer1','test','buyer1','B',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# user=User_Model('testbuyer2@testmail.com','testbuyer2','testbuyer2','test','buyer2','B',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# db.close()



