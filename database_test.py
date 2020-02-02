import shelve
from model import *
import os
import glob
from datetime import datetime
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
    db = shelve.open('database/forum_database/FAQDisplay.db','c')
    db.clear()
    db.close()
    db = shelve.open('database/forum_database/FAQQ.db','c')
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

# for i in range(29):
#     Add_New_Products('grey shirt',200,'very grey shirt',100,1,['male'],['mango-man-1156-4297221-1.jpg'])

# date = datetime.datetime.now()

# db = shelve.open('database/user_database/user.db', 'w')
# user=User_Model('testadmin@testmail.com','testadmin','testadmin','test','admin','A',datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# user=User_Model('testseller1@testmail.com','testseller1','testseller1','test','seller1','A',datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# user=User_Model('testseller2@testmail.com','testseller2','testseller2','test','seller2','A',datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# user=User_Model('testbuyer1@testmail.com','testbuyer1','testbuyer1','test','buyer1','B',datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# user=User_Model('testbuyer2@testmail.com','testbuyer2','testbuyer2','test','buyer2','B',datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
# db[user.get_user_id()]=user
# db.close()



def dbmanager():
    while True:
        print('===========================================================')
        print('Welcome to chaints database manager please choose an option')
        print('''1.delete and recreate all database \n2.create test users\n3.clear existing database data\n4.exit program ''')
        print('===========================================================')
        option = input('Please choose a option:')
        if option == '1':
            db_delete_confirm = input('Are you sure the change cannot ne undone  Y(yes)/N(no)')
            if db_delete_confirm.lower() == 'y':
                delete_all_db()
                init_all()
                print('all database are reset and recreated')
            elif db_delete_confirm.lower() == 'n':
                print('canceled')
            else:
                print('invalid input')
        elif option == '2':
            db = shelve.open('database/user_database/user.db', 'w')
            user=User_Model('testadmin@testmail.com','testadmin','testadmin','test','admin','A',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            db[user.get_user_id()]=user
            user=User_Model('testseller1@testmail.com','testseller1','testseller1','test','seller1','S',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            db[user.get_user_id()]=user
            user=User_Model('testseller2@testmail.com','testseller2','testseller2','test','seller2','S',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            db[user.get_user_id()]=user
            user=User_Model('testbuyer1@testmail.com','testbuyer1','testbuyer1','test','buyer1','B',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            db[user.get_user_id()]=user
            user=User_Model('testbuyer2@testmail.com','testbuyer2','testbuyer2','test','buyer2','B',datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            db[user.get_user_id()]=user
            db.close()
        elif option == '3':
            print('please select a databse to clear')
            print('===========================================================')
            print('1: User database\n2: Product database\n3: Cart database\n4: Order database\n5: Delivery database\n6: Carrier database\n7: FAQQ database\n8: Logs database')
            print('===========================================================')
            db_option = input('please select an option')
            if db_option == '1':
                 db = shelve.open('database/user_database/user.db','w')
                 db.clear()
                 db.close()
            elif db_option == '2':
                 db = shelve.open('database/product_database/product.db','w')
                 db.clear()
                 db.close()
            elif db_option == '3':
                 db = shelve.open('database/order_database/cart.db','w')
                 db.clear()
                 db.close()
            elif db_option == '4':
                 db = shelve.open('database/order_database/order.db','w')
                 db.clear()
                 db.close()
            elif db_option == '5':
                 db = shelve.open('database/delivery_database/delivery.db','w')
                 db.clear()
                 db.close()
            elif db_option == '6':
                 db = shelve.open('database/delivery_database/carrier.db','w')
                 db.clear()
                 db.close()
            elif db_option == '7':
                 db = shelve.open('database/forum_database/FAQQ.db','w')
                 db.clear()
                 db.close()
            elif db_option == '8':
                 db = shelve.open('database/logs_database/logs.db','w')
                 db.clear()
                 db.close()
            else:
                print('invalid input')
        elif  option == '4':
            break
dbmanager()
