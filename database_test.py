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