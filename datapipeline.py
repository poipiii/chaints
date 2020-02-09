import random
import shelve
import pandas as pd
import numpy as np
import time
from model import *


# db = shelve.open('database/logs_database/logs.db','r')
# for i in db:
#     print(i)
# db.close()




def get_all_order(productidlist):
    all_order_data = []
    db = shelve.open('database/logs_database/logs.db')
    for user in db.values():
        for order in user.get_order_log_list():
            if order.get_product_id() in productidlist:
                all_order_data.append(order)
            else:
                pass
    if len(all_order_data) > 0:
        return all_order_data
    else:
        return None


def current_week(p_year,p_week):
    mon = datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    tues = mon +timedelta(days=1)
    wed = mon + timedelta(days=2)
    thurs = mon + timedelta(days=3)
    fri =  mon + timedelta(days=4)
    sat = mon + timedelta(days=5)
    sun = mon + timedelta(days=6)
    return [mon,tues,wed,thurs,fri,sat,sun]


def to_df(ownp):
    orderdata = get_all_order(ownp)
    if orderdata is not None:
        df_data = []
        for i in orderdata:
            datadict = {'product_id':i.get_product_id(),'profit':i.get_o_profit(),'quantity':i.get_o_amount(),'datetime':i.get_timestamp_as_datetime().strftime("%Y/%m/%d %H:%M:%S")}
            df_data.append(datadict)
        df = pd.DataFrame(df_data)
        df = df.set_index(pd.DatetimeIndex(df['datetime'])).drop('datetime',axis=1)
        return df
    else:
        return None
def api_data_week(ownp):
    df = to_df(ownp)
    this_week = current_week(str(datetime.now().isocalendar()[0]),str(datetime.now().isocalendar()[1]))
    week = pd.DatetimeIndex(this_week)
    week_data = df.groupby(week[week.searchsorted(df.index)]).sum().to_json(date_format = 'iso')
    return week_data   

def api_data_month(ownp):
    df = to_df(ownp)
    month_data = df.profit.resample('M').sum().to_json(date_format = 'iso')

    return month_data

def api_data_year(ownp):
    df = to_df(ownp)
    year_data = df.profit.resample('Y').sum().to_json(date_format = 'iso')
    return year_data  

 
def api_all_profit(ownp):
    total_profit = {}
    df = to_df(ownp)
    if df is not None:
        this_week = current_week(str(datetime.now().isocalendar()[0]),str(datetime.now().isocalendar()[1]))
        week = pd.DatetimeIndex(this_week)
        week_data = df.groupby(week[week.searchsorted(df.index)]).sum().to_dict()
        total_profit['week'] = sum(week_data['profit'].values())
        month =  df.profit.resample('M').sum().to_dict()
        print(month)
        for i in month:
            if i.to_pydatetime().strftime('%m') == datetime.now().strftime('%m'):
                print(i)
                total_profit['month'] =month[i]
                print(month[i])
        total_profit['year']= df.profit.resample('Y').sum().iloc[0]
        return total_profit
    else:
        return 0






# def test_func():
#     df = to_df(ownp)
#     test = current_week(str(datetime.now().isocalendar()[0]),str(datetime.now().isocalendar()[1]))
#     test_week = pd.DatetimeIndex(test)
#     custom_sum = df.groupby(test_week[test_week.searchsorted(df.index)]).sum().to_json(date_format = 'iso')
#     monthdata = df.profit.resample('M').sum().to_json(date_format = 'iso')
#     yeardata = df.profit.resample('Y').sum().to_json(date_format = 'iso')
#     return yeardata



# def data_api(owned_products,dtype,date):
#     all_own_products = get_all_order(owned_products)
#     if dtype == 'DAY':
#         sorted_list = datesort(date,all_own_products)
#     elif dtype == 'WEEK':
#         sorted_list = weeksort(date,all_own_products)
#     elif dtype == 'MONTH':
#         sorted_list = monthsort(date,all_own_products)
#     elif dtype == 'YEAR':
#         sorted_list = yearsort(date,all_own_products)
#     else:
#         sorted_list = None
#     return sorted_list

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

# def datesort(date,df):
#     return df[date].profit.resample('H').sum().to_json(date_format = 'iso')
# def weeksort(df):
#     orders = ownp
#     sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().isocalendar()[1] == datetime.strptime(date,'%Y-%m-%d').isocalendar()[1] and order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
#     return list(sort_by_date)

# def monthsort(df):
#     orders = ownp
#     sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().strftime('%m') == datetime.strptime(date,'%Y-%m-%d').strftime('%m') and order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
#     return list(sort_by_date)


# def yearsort(df):
#     orders = ownp
#     sort_by_date = filter(lambda order: order.get_timestamp_as_datetime().strftime('%Y') == datetime.strptime(date,'%Y-%m-%d').strftime('%Y'),orders)
#     return list(sort_by_date)





# def getDateRangeFromWeek(p_year,p_week):
#     firstdayofweek = datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
#     lastdayofweek = firstdayofweek + timedelta(days=2)
    
#     return firstdayofweek, lastdayofweek


#Call function to get dates range 
# def current_week(p_year,p_week):
#     mon = datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
#     mon = datetime.combine(mon,datetime.min.time())
#     tues = datetime.combine(mon+timedelta(days=1),datetime.min.time())
#     wed = datetime.combine(mon+timedelta(days=2),datetime.min.time()) 
#     thurs = datetime.combine(mon+timedelta(days=3),datetime.min.time())
#     fri =  datetime.combine(mon+timedelta(days=4),datetime.min.time())
#     sat = datetime.combine(mon+timedelta(days=5),datetime.min.time())
#     sun = datetime.combine(mon+timedelta(days=6),datetime.min.time())
#     return [mon,tues,wed,thurs,fri,sat,sun]
# test = current_week(str(datetime.now().isocalendar()[0]),str(datetime.now().isocalendar()[1]))
# print(test)
# test_week = pd.DatetimeIndex(test)

# all_own_products = get_all_order(owned_products)
# totalinday = 0
# for item in all_own_products
#     if item.get_timestamp_as_datetime() == test_week[0]:
#         totalinday +=









# def months(year):
#     monthlist = []
#     for i in range(12):
#         monthlist.append(str(year)+'-'+str(i+1))
#     print(monthlist)
# months(2020)
# df = to_df(ownp)

# print(df.profit.resample('M').sum().to_json(date_format = 'iso'))
# custom_sum = df.groupby(test_week[test_week.searchsorted(df.index)]).sum().to_json(date_format = 'iso')

# print(df.head())
# custom_sum = df.groupby(test_week[test_week.searchsorted(df.index)]).sum().to_json()
# print(custom_sum)
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


# def get_all_users_id():
#     userlst = ['e633e7da22b44fb5a70ee529679acb80','f4d5bb79756d444eb6ab8db8adb3bd5a']
#     return userlst

# testdatau = get_all_users_id()
# for i in range(10):
#     order_logging(random.choice(testdatau),random.randint(1,20),'15331c30ca594ecdad14393ee515a130','TEST')
#     order_logging(random.choice(testdatau),random.randint(1,20),'1779fa11dd0b421498431b2a8ec4490c','TEST')
