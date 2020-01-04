import shelve
from model import *
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


