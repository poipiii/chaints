#user account details
#user model - email,username,password,orders,payment,address
#orders - item,price,quantity, order id
import random
class User:
    def __init__(self,email,username,password,firstname,lastname):
        self.__email=email
        self.__username=username
        self.__password=password
        self.__firstname=firstname
        self.__lastname=lastname
        self.__userID=random.randint(10000,99999)

    def set_email(self,email):
        self.__email=email

    def set_username(self,username):
        self.__username=username

    def set_password(self,password):
        self.__password=password

    def set_firstname(self,firstname):
        self.__firstname=firstname

    def set__lastname(self,lastname):
        self.__lastname=lastname

    def get_email(self):
        return self.__email

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_firstname(self):
        return self.__firstname

    def get_lastname(self):
        return self.__lastname

    def get_fullname(self):
        return self.__firstname+" "+self.__lastname





