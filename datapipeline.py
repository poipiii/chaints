import random
import shelve
import pandas as pd
import numpy as np
from model import *


# db = shelve.open('database/logs_database/logs.db','r')
# for i in db:
#     print(i)
# db.close()

def get_all_users_id():
    userlst = ['6bbf25a90bfd4baab5ef5e764f5b7753','49aa66e5bf71407daa1c6e91f41cbdb6']
    return userlst

# testdatau = get_all_users_id()
# for i in range(2):
#     order_logging(random.choice(testdatau),random.randint(1,20),'ba2f9310e9e64230890298ffe4f20401','TEST')


def get_all_order(productidlist):
    all_order_data = []
    db = shelve.open('database/logs_database/logs.db')
    for user in db.values():
        for order in user.get_order_log_list():
            if order.get_product_id() in productidlist:
                all_order_data.append(order)
            else:
                pass
    return all_order_data

def api_get_all(owned_products,dtype,date):
    all_own_products = get_all_order(owned_products)
    if dtype == 'DAY':
        sorted_list = datesort(date,all_own_products)
    elif dtype == 'WEEK':
        sorted_list = weeksort(date,all_own_products)
    elif dtype == 'MONTH':
        sorted_list = monthsort(date,all_own_products)
    elif dtype == 'YEAR':
        sorted_list = yearsort(date,all_own_products)
    else:
        sorted_list = None
    return sorted_list

# def datesort(date,ownp):
#     orders = ownp
#     sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().strftime("%Y-%m-%d") == date, orders)
#     return list(sort_by_date)
# def weeksort(date,ownp):
#     orders = ownp
#     sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().isocalendar()[1] == datetime.strptime(date,'%Y-%m-%d').isocalendar()[1] and order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
#     return list(sort_by_date)

# def monthsort(date,ownp):
#     orders = ownp
#     sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().strftime('%m') == datetime.strptime(date,'%Y-%m-%d').strftime('%m') and order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
#     return list(sort_by_date)


# def yearsort(date,ownp):
#     orders = ownp
#     sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
#     return list(sort_by_date)

def datesort(date,df):
    return df[date].profit.resample('H').sum().to_json(date_format = 'iso')
def weeksort(df):
    orders = ownp
    sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().isocalendar()[1] == datetime.strptime(date,'%Y-%m-%d').isocalendar()[1] and order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
    return list(sort_by_date)

def monthsort(df):
    orders = ownp
    sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().strftime('%m') == datetime.strptime(date,'%Y-%m-%d').strftime('%m') and order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
    return list(sort_by_date)


def yearsort(df):
    orders = ownp
    sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
    return list(sort_by_date)


ownp = ['d97db4c0ab7a4e75935fd6bb7a8e8f51','7ee8e6589fa24898af240be7ff546f14','ba2f9310e9e64230890298ffe4f20401']
def to_df(ownp):
    orderdata = get_all_order(ownp)
    df_data = []
    for i in orderdata:
        datadict = {'product_id':i.get_product_id(),'profit':i.get_o_profit(),'quantity':i.get_o_amount(),'datetime':i.get_timestamp_as_datetime().strftime("%Y/%m/%d %H:%M:%S")}
        df_data.append(datadict)
    df = pd.DataFrame(df_data)
    df = df.set_index(pd.DatetimeIndex(df['datetime'])).drop('datetime',axis=1)
    return df

# df = to_df(ownp)
# test2 = df.set_index(pd.DatetimeIndex(df['datetime'])).drop('datetime',axis=1)
# print(test2.profit.resample('Y').sum().to_json(date_format = 'iso'))





# def test_func():
#     test2 = get_order_log_by_id('3e5b28fe29024a978501ce65c3936f13')
#     profit = []
#     time = []
#     for i in test2:
#         profit.append(i.get_o_profit())
#         time.append(i.get_timestamp_as_datetime().strftime("%m/%d/%Y %H:%M:%S"))
#     sales = [profit,time]
#     return sales



# def test_func():
#     test2 = get_order_log_by_id('3e5b28fe29024a978501ce65c3936f13')
#     sales = []
#     for i in test2:
#         sale_data = to_df(i.get_product_id(),i.get_o_profit(),i.get_o_amount(),i.get_timestamp_as_datetime())
#         sales.append(sale_data)
#     df = pd.DataFrame(sales)
#     df_test = df.drop(['product_id','quantity'],axis=1)
#     return df_test