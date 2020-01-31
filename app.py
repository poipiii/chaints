import shelve
from flask import *
import os
from Forms import *
from werkzeug.datastructures import CombinedMultiDict,FileStorage
from werkzeug import secure_filename
from model import *
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from datapipeline import *

from Forms import Question, Response
app = Flask(__name__)
app.secret_key = "sadbiscuit"
app.config["PRODUCT_IMAGE_UPLOAD"] = "static/product_images"
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'tasky.webapp@gmail.com',
	MAIL_PASSWORD = '7eNGs-Z76#G-LKFV?PP@@NwkzraC$egq'
	)
s= URLSafeTimedSerializer(app.secret_key)
mail = Mail(app)
@app.before_request
def before_request():
    if session.get('logged_in') == True:
        if session.get('remember')==True:
            pass
    else:
        now = datetime.now()
        try:
            last_active = session['last_active']
            delta = now - last_active
            if delta.seconds > 1800:
                session['last_active'] = now
                session['forced_logout']= True
        except:
            pass

        try:
            session['last_active'] = now
        except:
            pass

#product display currently not working ui not done yet can do other stuff still will not affect
@app.route("/")
def landing_page():
    Products = fetch_products()
    womenlist =[]
    childernlist= []
    menlist = []
    for i in Products:
        if 'female' in i.get_product_catergory():
            womenlist.append(i)
        if 'male'in i.get_product_catergory():
            menlist.append(i)

        if 'child'in i.get_product_catergory():
            childernlist.append(i)
    print(menlist)
    return render_template('home_page.html' ,product_list = Products,women = womenlist,men = menlist,child = childernlist )



#currently not working ui not done yet whatsapp me before touching this  
@app.route("/product/<productid>")
def product_page(productid):
    get_product = get_product_by_id(productid)
    seller = get_user(get_product.get_seller_id())
    return render_template('productdetails.html',product = get_product,sellerinfo = seller.get_username() )

#only be able to access if session['logged_in']==True


@app.route("/catergories")
def catergory_page():
    Products = fetch_products()
    return render_template('productcatergory.html',product_list = Products)

@app.route("/catergories/<catergory_type>")
def sorted_catergory_page(catergory_type):
    sorted_list = []
    Products = fetch_products()
    for i in Products:
        if catergory_type in i.get_product_catergory():
            sorted_list.append(i)
    return render_template('productcatergory.html',product_list = sorted_list)



@app.route("/details")
def details_page():
    return render_template('productdetails.html')




@app.route("/dashboard")
def dashboard_home():
    return render_template('chart.html')

@app.route("/data/<d_type>")
def datapipe(d_type):
    if session.get('role') == 'A':
        ownp = get_usr_owned_p(session.get('user_id'))
        if d_type == 'week':
            chart_data = api_data_week(ownp)
            return chart_data
        elif d_type == 'month':
            chart_data = api_data_month(ownp)
            return chart_data
        elif d_type == 'year':
            chart_data = api_data_year(ownp)
            return chart_data
        else:
             return None
    else:
        return None

@app.route("/apitest")
def datatest():
    ownp = ['a9ee20758e2647f69d3bbf92066f3d31']
    if request.args.get('type') == 'ALL':
        apidata = api_get_all(ownp,request.args.get('datetype'),request.args.get('date'))
        if apidata is not None:
            profit = []
            dtime = []
            for orders in apidata:
                profit.append(orders.get_o_profit())
                dtime.append(orders.get_timestamp_as_datetime().strftime("%m/%d/%Y %H:%M:%S"))
            return jsonify({"profit":profit},{"datetime":dtime})
        else:
            return jsonify({"profit":None},{"datetime":None})

    else:
        return jsonify({"profit":None},{"datetime":None})




    # apidata = api_func()
    # profit = apidata[0]
    # dtime = apidata[1]
    # return jsonify({"profit":profit},{"datetime":dtime})


@app.route("/product_logs")
def dashboard_logs():
    product_log = get_product_log_by_id(session.get('user_id'))
    if product_log is not None:
        user_id = session.get('user_id')
        return render_template('staff_logs_page.html',product_log_list = product_log,userid = user_id )
    else:
        return render_template('productlognone.html')

@app.route("/manage_products",methods=['POST', 'GET'])
def dashboard_products():
    Products = fetch_products_by_user(session.get('user_id'))
    return render_template('staff_product_page.html',product_list = Products)

#route to create new product form
@app.route("/create_products",methods=['POST', 'GET'])
def product_create():
    #take in more than 1 images from form, rename images and upload to static/product_images
    Product_Form = Create_Product_Form(CombinedMultiDict((request.files, request.form)))
    filenames = []
    if request.method == 'POST' and Product_Form.validate() :
        #product_pics = request.files.getlist(Product_Form.product_images)
        product_pics = Product_Form.product_images.data
        for i in product_pics:
            #TODO 
             filename = secure_filename(i.filename)
             i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
             filenames.append(filename)
        print(filenames)
        new_product = Add_New_Products(session.get('user_id'),Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)  
        flash('Product successfully created')
        return redirect(url_for('dashboard_products'))      
    return render_template('productcreateform.html',form =Product_Form ,ftype = 'create')

    
#route to update product form
@app.route("/update_products/<productid>",methods=['POST', 'GET'])
def dashboard_edit_products(productid):
    original_product =  get_product_by_id(productid)
    Product_Form = Edit_Product_Form(CombinedMultiDict((request.files, request.form)))
    filenames = []
    #take in more than 1 images from form, rename images and upload to static/product_images
    if request.method == 'POST'  and Product_Form.validate():
        #product_pics = request.files.getlist(Product_Form.product_images)
        product_pics = Product_Form.product_images.data
        check_if_empty = [i.filename for i in product_pics]
        if '' in check_if_empty:
            Edit_Products(session.get('user_id'),productid,Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,original_product.get_product_images())
        else:
            for i in product_pics:
                #TODO 
                 filename = secure_filename(i.filename)
                 i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
                 filenames.append(filename)
            #pass form data to Edit_Products function in model.py
            Edit_Products(session.get('user_id'),productid,Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)
        flash('Product successfully updated')
        return redirect(url_for('dashboard_products')) 
    else:
        Product_Form.product_name.data = original_product.get_product_name()
        Product_Form.product_Quantity.data = original_product.get_product_current_qty()
        Product_Form.product_Description.data = original_product.get_product_desc()
        Product_Form.product_Selling_Price.data = original_product.get_product_price()
        Product_Form.product_Discount.data = original_product.get_product_discount()
        Product_Form.product_catergory.data = original_product.get_product_catergory()
        Product_Form.product_images.data = original_product.get_product_images()
    return render_template('productcreateform.html',form =Product_Form,ftype ='update')

@app.route("/updateqty/<productid>",methods=['POST', 'GET'])
def updateqty(productid):
    original_product =  get_product_by_id(productid)
    updateqty_form = update_Quantity_Form(request.form)
    if request.method == 'POST'  and updateqty_form.validate():
        updatequantity(session.get('user_id'),productid,updateqty_form.product_Quantity.data)
        flash('Product quantity successfully updated')
        return redirect(url_for('dashboard_products')) 

    else:
        updateqty_form.product_Quantity.data = original_product.get_product_current_qty()
    return render_template('updateqtyform.html',form =updateqty_form)



#take in product id and delete product from shelve  
@app.route("/delete_products/<productid>",methods=['POST'])
def delete_products(productid):
    delete_product_by_id(productid,session.get('user_id'))
    flash('Product successfully deleted')
    return redirect(url_for('dashboard_products'))

@app.route("/review",methods = ['POST','GET'])
def review():
    Review_form = review_form(request.form)
    if request.method == 'POST'  and Review_form.validate():
        print(int(Review_form.rating.data))
        add_review(session.get('user_id'),session.get('name'),'a9ee20758e2647f69d3bbf92066f3d31',int(Review_form.rating.data),Review_form.review_text.data)
        return redirect(url_for('landing_page'))
    return render_template('review_form.html',form = Review_form)


#User Management
#sign up user
@app.route('/signup', methods=['GET', 'POST'])

def signupUser():
    if session.get('logged_in')==True:
        return redirect(url_for("landing_page"))
    createUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and createUserForm.validate():
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname= request.form['firstname']
        lastname= request.form['lastname']
        role= request.form['role']
        user = (email,username,password,firstname,lastname,role)
        token=s.dumps(user,salt='email-confirm')
        msg=Message(subject='Confirm Email', sender='tasky.webapp@gmail.com', recipients=[email])
        link = url_for('confirm_email',token=token, _external=True)
        msg.body ='Your link is {}'.format(link)
        mail.send(msg)
        flash('An email has been sent. Please verify your account before logging in')
        return redirect(url_for("landing_page"))
    return render_template('Signup.html', form=createUserForm)

#retrieve User to check db if input correctly
#will move it to admin side after ui finished
@app.route('/confirm_email/<token>')
def confirm_email(token):
    now=datetime.now()
    date=now.strftime("%d/%m/%Y, %H:%M:%S")
    user=s.loads(token,salt='email-confirm',max_age=300)
    db = shelve.open('database/user_database/user.db', 'c')
    user=User_Model(user[0],user[1],user[2],user[3],user[4],user[5],date)
    db[user.get_user_id()]=user
    db.close()
    flash('Your account has been verified')
    return redirect(url_for("landing_page"))

@app.route('/retrieveUsers')
def retrieveUsers():
    db = shelve.open('database/user_database/user.db', 'r')
    usersList = []
    for user in db:
        user=db[user]
        usersList.append(user)
    db.close()

    return render_template('retrieveUsers.html',usersList=usersList, count=len(usersList))

@app.route('/passwordreset_email',methods=['GET','POST'])
def passwordreset_email():
    getEmailForm = GetEmailForm(request.form)
    if request.method == 'POST' and getEmailForm.validate():
        email=request.form['email']
        db = shelve.open('database/user_database/user.db', 'r')
        for user in db:
            user=db[user]
            if email==user.get_user_email():
                userid = user.get_user_id()
                token=s.dumps(userid,salt='password_reset')
                msg=Message(subject='Password Reset', sender='tasky.webapp@gmail.com', recipients=[email])
                link = url_for('create_newpassword',token=token, _external=True)
                msg.body ='Your Password Reset link is {}'.format(link)
                mail.send(msg)
                db.close()
                flash('An email has been sent. Please check your email to reset your password')
                return redirect(url_for("loginUser"))
        db.close()
    return render_template('passwordreset_email.html',form=getEmailForm)



@app.route('/create_newpassword/<token>',methods=['GET','POST'])
def create_newpassword(token):
    getPasswordForm=PasswordReset(request.form)
    if request.method == 'POST' and getPasswordForm.validate():
        userid =s.loads(token,salt='password_reset',max_age=300)
        db = shelve.open('database/user_database/user.db', 'w')
        user=db[userid]
        pw=request.form['password']
        user.set_user_pw(pw)
        db[userid]=user
        db.close()
        flash('Your password has been reset')
        return redirect(url_for("loginUser"))
    return render_template('create_newpassword.html', form=getPasswordForm)



#login user, session['logged_in']==True here
@app.route('/login', methods=['GET', 'POST'])

def loginUser():
    if session.get('logged_in')==True:
        return redirect(url_for("landing_page"))
    else:
        createLoginForm = CreateLoginForm(request.form)
        if request.method == 'POST' and createLoginForm.validate():
                db = shelve.open('database/user_database/user.db', 'r')
                username = request.form['username']
                pw = request.form['password']
                for user in db:
                    user=db[user]
                    if user.get_username()==username and pbkdf2_sha256.verify(pw,user.get_user_pw())==True:
                        session['logged_in'] = True
                        session['user_id']=user.get_user_id()
                        session['name']=user.get_user_fullname()
                        session['role']=user.get_user_role()
                        session['profile_picture']=user.get_user_profile_picture()
                        db.close()
                        try:
                            if request.form['remember']:
                                session['remember']=True
                        except:
                            pass
                        return redirect(url_for('landing_page'))
                db.close()
                error = 'Invalid Credentials. Please try again.'
                return render_template('login.html', form=createLoginForm, error=error)
        return render_template('login.html', form=createLoginForm)


#pop the session['logged_in'] out so will redirect to normal main page
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing_page'))



@app.route('/updateUser/<id>', methods=['GET', 'POST'])
def updateUser(id):
    updateUserForm = CreateUpdateForm(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        db = shelve.open("database/user_database/user.db", "w")
        user = db[id]
        user.set_user_email(updateUserForm.email.data)
        user.set_username(updateUserForm.username.data)
        user.set_user_firstname(updateUserForm.firstname.data)
        user.set_user_lastname(updateUserForm.lastname.data)
        user.set_user_role(updateUserForm.role.data)
        db[id]=user

        db.close()
        return redirect(url_for("retrieveUsers"))
    else:
        db = shelve.open('database/user_database/user.db', 'r')
        user = db[id]
        updateUserForm.email.data = user.get_user_email()
        updateUserForm.username.data = user.get_username()
        updateUserForm.firstname.data = user.get_user_firstname()
        updateUserForm.lastname.data = user.get_user_lastname()
        updateUserForm.role.data = user.get_user_role()
        db.close()
        return render_template('updateUser.html',form=updateUserForm)

@app.route('/deleteUser/<id>', methods=['POST'])
def deleteUser(id):
 db = shelve.open('database/user_database/user.db', 'w')
 db.pop(id)
 db.close()
 return redirect(url_for('retrieveUsers'))


#adding  product to cart 
@app.route('/profile')
def profile():
    db = shelve.open('database/user_database/user.db', 'r')
    usersList = []
    for user in db:
        user=db[user]
        usersList.append(user)
    db.close()

    return render_template('profile.html',usersList=usersList, count=len(usersList))



#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
#Order Management
@app.route('/add_to_cart/<productid>/<int:productqty>')
def Add_to_cart(productid,productqty):
    #take in productid and product quantity from route 
    db= shelve.open('database/order_database/cart.db','c')
    #check if logged in user is in cart db 
    if session.get('user_id')in db:
        # if user record exist fetch it from cart db and put it in varible usercart
        #the record will be a dict
        usercart=db.get(session.get('user_id'))
    else:
        #if user record does not exist usercart is a empty dict 
        usercart={}
    #if productid in usercart dict add on to the quantity 
    if productid in usercart.keys():
        usercart[productid] += productqty
    else:
        #if does not exist add it to the usercart dict with product id as key and quantity as value 
        usercart[productid] = productqty
    #save the record to the cart db with current logged in user id as key and usercart dict as value 
    db[session.get('user_id')] = usercart
    db.close()
    return redirect(url_for('landing_page'))

@app.route('/cart')
def cart():
    #initalise a empty list for product objects in varible productincart
    productincart = []
    db=shelve.open('database/order_database/cart.db','c')
    # if user record exist fetch it from cart db and put it in varible usercart
    if session.get('user_id')in db:
        usercart=db.get(session.get('user_id'))
        print(usercart)
        #retrive product object from product db using the product id stored in usercart dict
        for item in usercart.keys():
            productincart.append(get_product_by_id(item))
    else:
        #if user record does not exist , usercart is initalise as a empty dict
        # and save empty dict to db so if user open cart without adding items there will be no error  
        usercart={}
        db[session.get('user_id')] = usercart

    db.close()
    return render_template('Add_To_Cart.html',usercart = usercart,productincart = productincart)


@app.route('/deletecart/<cartproductid>',methods = ['POST'])
#take in post request from the route and the product id of the item to be deleted 
def deletecart(cartproductid):
    db = shelve.open('database/order_database/cart.db','w')
    # if user record exist fetch it from cart db and put it in varible usercart
    if session.get('user_id') in db:
        usercart = db.get(session.get('user_id'))
        #delete the product from the usercart dict using pop and passing in the key of the product to be deleted 
        usercart.pop(cartproductid)
        #save the upadted dict to the cart db 
        db[session.get('user_id')] = usercart
    else:
        raise 'user does not have a cart created'
    return redirect(url_for('cart'))







@app.route('/Deliverydetails',methods=['GET','POST'])
def Deliverydetails():
    DeliveryForm= DeliveryForm(request.form)
    if request.method=="POST" and DeliveryForm.validate():
        return render_template('Payment.html',form=DeliveryForm)
    else:
        return redirect(url_for('Deliverydetails'))





#Delivery Management

@app.route('/SellerDelivery')
def seller_deliverylist():
    userid=session.get('user_id')
    db=shelve.open('database/user_database/user.db','r')
    if db[userid].get_user_role()!="A":
        return redirect(url_for('buyer_deliverylist'))
    db.close()
    delivery_list=create_seller_order_list(session.get('user_id'))
    return render_template('seller_delivery_status.html',delivery_list=delivery_list)
#add in additional codes to read data from database :(

@app.route('/SellerDeliveryUpdate/<orderid>',methods=['POST','GET'])
def delivery_status_update(orderid):
    updatedstatusform= NewStatus(request.form)
    try:
        db=shelve.open('database/delivery_database/delivery.db', 'c')
        sellerorderlist=create_seller_order_list(session.get('user_id'))
        for i in sellerorderlist:
            if i.get_individual_orderid()==orderid:
                orderobj=i
        db.close()
    except IOError:
        print("ERROR db no exist")
    except:
        print("Some unknown error happened i guess")
    if request.method=='POST' and updatedstatusform.validate():
        passing_app_to_update(orderid,updatedstatusform.deliverystatus.data)
        return redirect(url_for('seller_deliverylist'))
    return render_template('seller_update_status.html',orderid=orderid,individual_order=orderobj,form=updatedstatusform)

@app.route('/BuyerDelivery')
def buyer_deliverylist():
    userid=session.get('user_id')
    deliverylist=create_buyer_order_list(userid)
    print(deliverylist)
    return render_template('buyer_delivery_status.html',deliverylist=deliverylist)


@app.route('/BuyerDeliveryDetails/<orderid>')
def buyer_deliverydetails(orderid):
    try:
        db=shelve.open('database/delivery_database/delivery.db', 'c')
        buyerorderlist=create_buyer_order_list(session.get('user_id'))
        for i in buyerorderlist:
            if i.get_individual_orderid()==orderid:
                orderobj=i
        db.close()
        db=shelve.open('database/delivery_database/carrier.db','c')
        if orderid in db:
            statuslist=db[orderid]
            db.close()
            return render_template('buyer_order_details.html',individual_order=orderobj,statuslist=statuslist)
        return render_template('buyer_order_details2.html',individual_order=orderobj)
    except IOError:
        print("db does not exist")
    except:
        print("an unknown error occurred")

@app.route('/DeletingDelivery/<orderid>')
def deleting_delivery(orderid):
    userid=session.get('user_id')
    cancelling_carrier_side(orderid)
    db=shelve.open('database/delivery_database/delivery.db', 'c')
    deliverylist=db[userid]
    for i in deliverylist:
        if i.get_individual_orderid()==orderid:
            deliverylist.remove(i)
    db[userid]=deliverylist
    db.close()
    return redirect(url_for('buyer_deliverylist'))


@app.route('/DeliveryReceived/<orderid>/<productid>')
def received_delivery(orderid,productid):
    userid=session.get('user_id')
    status_update(productid,userid,"Order Received")
    deliverylist=create_buyer_order_list(userid)
    return redirect(url_for('buyer_deliverylist'))


@app.route('/CarrierUpdate', methods=['GET','POST'])
def CarrierUpdate():
    carrierupdateform=CarrierForm(request.form)
    if request.method=='POST' and carrierupdateform.validate():
        updatedate=carrierupdateform.updatedate.data
        country=carrierupdateform.country.data
        status=carrierupdateform.status.data
        deliverynotes=carrierupdateform.deliverynotes.data
        orderid=carrierupdateform.orderid.data
        db=shelve.open('database/delivery_database/delivery.db','c')
        checker=False
        for i in db:
            for n in db[i]:
                if n.get_individual_orderid()==orderid:
                    checker=True
                    address=n.get_address()
        db.close()
        if checker==True:
            carrierobj_and_db(orderid,updatedate,country,status,deliverynotes,address)
            return render_template('testing2.html')
        else:
            return render_template('carrier_update.html',form=carrierupdateform)
    return render_template('carrier_update.html',form=carrierupdateform)






#FAQ Display
@app.route('/FAQ')
def FAQ():
    Gold=[]
    FaQ=[]
    AcI=[]
    CoI=[]
    try:
        Ein=shelve.open("database/forum_database/FAQQ.db","r")
        Enamel=Ein.values()
        for i in Enamel:
            if isinstance(i,CQuestion):
                Gold.append(i)

        Ein.close()
    except:
        print("A Database not found")
    try:
        Zwei=shelve.open("database/forum_database/FAQDisplay.db","r")
        Endeavour=Zwei.values()
        for i in Endeavour:
            if isinstance(i,FAQm):
                FaQ.append(i)
            elif isinstance(i,Account_Issues):
                AcI.append(i)
            elif isinstance(i,Contact):
                CoI.append(i)
        Zwei.close()
    except:
        print("A Database not found")
    return render_template('FAQ.html', Gold=Gold, FaQ=FaQ , AcI=AcI,CoI=CoI)


#Forum Question
@app.route('/createQns',methods=["GET","POST"])
def createQns():
    createquestion=Question(request.form)
    if request.method=="POST" and createquestion.validate():
        new_question = CQuestion(session.get('user_id'),createquestion.mtitle.data,createquestion.mbody.data)
        try:
            db=shelve.open('database/forum_database/FAQQ.db','c')
            db[new_question.get_msgid()] = new_question
        except IOError:
            print("Database failed to open")
        db.close()
        return redirect(url_for('FAQ'))
    return render_template('createQns.html',form=createquestion)
#Forum Answer
@app.route('/Respond/<id>',methods=["GET","POST"])
def Respond(id):
    Reply=Response(request.form)
    if request.method=="POST" and Reply.validate():
        Respondents= CAnswer(session.get('user_id'),"",Reply.Response.data)
        try:
            dennis=shelve.open('database/forum_database/FAQQ.db','c')
            dennis[Respondents.get_ansid()]=Respondents
        except:
            print("Something screwed up")
        dennis.close()
        RespondtoQns(Respondents.get_ansid(),id)
        return redirect(url_for('displayQns',id=id))
    return render_template('Response.html',form=Reply)

@app.route('/displayQns/<id>')
def displayQns(id):
    question = get_question_by_id(id)
    AnswerList=get_answer_by_id(question.get_ans_list())
    return render_template('displayQns.html',question = question, AnswerList=AnswerList)

#update Qns in Forum
@app.route('/updateQns/<id>',methods=["GET","POST"])
def updateQns(id):
    updateQns=Question(request.form)
    if request.method =='POST' and updateQns.validate():
        db=shelve.open('database/forum_database/FAQQ.db','w')
        Qns= db.get(id)
        Qns.setmtitle(updateQns.mtitle.data)
        Qns.setmbody(updateQns.mbody.data)
        db[id]= Qns
        db.close()
        return redirect(url_for('FAQ'))
    else:
        db= shelve.open('database/forum_database/FAQQ.db','r')
        Qns= db.get(id)
        db.close()
        updateQns.mtitle.data= Qns.getmtitle()
        updateQns.mbody.data=Qns.getmbody()
        return render_template('updateqns.html',form=updateQns)

@app.route('/addFAQueryFaQ',methods=["GET","POST"])
def addFAQueryF():
    Drei=FAQd(request.form)
    if request.method=="POST" and Drei.validate():

        Able=FAQm(Drei.question.data,Drei.answer.data)
        try:
            Three=shelve.open("database/forum_database/FAQDisplay.db","c")
            Three[Able.getid()] = Able
            
        except IOError:
            print("ooopsie")
        Three.close()
        return redirect(url_for('FAQ'))
    return render_template('faqopening1.html',form=Drei)

@app.route('/addFAQueryAcI',methods=["GET","POST"])
def addFAQueryAcI():
    Vier=FAQd(request.form)
    if request.method=="POST" and Vier.validate():
        Baker=Account_Issues(Vier.question.data,Vier.answer.data)
        try:
            Four=shelve.open("database/forum_database/FAQDisplay.db","c")
            Four[Baker.getid()] = Baker
            
        except IOError:
            print("ooopsie")
        Four.close()
        return redirect(url_for('FAQ'))
    return render_template('faqopening1.html',form=Vier)

@app.route('/addFAQueryCoI',methods=["GET","POST"])
def addFAQueryCoI():
    Fuenf=FAQd(request.form)
    if request.method=="POST" and Fuenf.validate():

        Charlie=Contact(Fuenf.question.data,Fuenf.answer.data)
        try:
            Five=shelve.open("database/forum_database/FAQDisplay.db","c")
            Five[Charlie.getid()] = Charlie
            
        except IOError:
            print("ooopsie")
        Five.close()
        return redirect(url_for('FAQ'))
    return render_template('faqopening1.html',form=Fuenf)

#update Qns in Forum
@app.route('/updateFAQueryF/<id>',methods=["GET","POST"])
def updateFAQueryF(id):
    updateFAQueryF=FAQd(request.form)
    if request.method =='POST' and updateFAQueryF.validate():
        db=shelve.open('database/forum_database/FAQDisplay.db','w')
        Fa= db.get(id)
        Fa.setquestion(updateFAQueryF.question.data)
        Fa.setanswer(updateFAQueryF.answer.data)

        db[id]= Fa
        db.close()
        
        return redirect(url_for('FAQ'))
        
    else:
        db= shelve.open('database/forum_database/FAQDisplay.db','r')
        Qns= db.get(id)
        db.close()
        
        updateFAQueryF.question.data= Qns.getquestion()
        updateFAQueryF.answer.data=Qns.getanswer()
        return render_template('faqopening2.html',form=updateFAQueryF)

#update Qns in Forum
@app.route('/updateFAQueryA/<id>',methods=["GET","POST"])
def updateFAQueryA(id):
    updateFAQueryA=FAQd(request.form)
    if request.method =='POST' and updateFAQueryA.validate():
        db=shelve.open('database/forum_database/FAQDisplay.db','w')
        Fa= db.get(id)
        Fa.setquestion(updateFAQueryA.question.data)
        Fa.setanswer(updateFAQueryA.answer.data)

        db[id]= Fa
        db.close()
        
        return redirect(url_for('FAQ'))
        
    else:
        db= shelve.open('database/forum_database/FAQDisplay.db','r')
        Qns= db.get(id)
        db.close()
        
        updateFAQueryA.question.data= Qns.getquestion()
        updateFAQueryA.answer.data=Qns.getanswer()
        return render_template('faqopening2.html',form=updateFAQueryA)

#update Qns in Forum
@app.route('/updateFAQueryC/<id>',methods=["GET","POST"])
def updateFAQueryC(id):
    updateFAQueryC=FAQd(request.form)
    if request.method =='POST' and updateFAQueryC.validate():
        db=shelve.open('database/forum_database/FAQDisplay.db','w')
        Fa= db.get(id)
        Fa.setquestion(updateFAQueryC.question.data)
        Fa.setanswer(updateFAQueryC.answer.data)

        db[id]= Fa
        db.close()
        
        return redirect(url_for('FAQ'))
        
    else:
        db= shelve.open('database/forum_database/FAQDisplay.db','r')
        Qns= db.get(id)
        db.close()
        
        updateFAQueryC.question.data= Qns.getquestion()
        updateFAQueryC.answer.data=Qns.getanswer()
        return render_template('faqopening2.html',form=updateFAQueryC)

@app.route('/deleteQns/<id>')
def deleteQns(id):
    Ace=shelve.open('database/forum_database/FAQDisplay.db','w')
    Ace.pop(id)
    Ace.close()
    
    return redirect(url_for('FAQ'))


@app.route('/deleteForumQns/<id>')
def deleteForumQns(id):
    Ace=shelve.open('database/forum_database/FAQQ.db','w')
    ri= Ace[id]
    
    for i in ri.get_ans_list():
        Ace.pop(i)

    Ace.pop(id)
    Ace.close()
    
    return redirect(url_for('FAQ'))

# @app.errorhandler(404)
# def not_found_error(error):  
#     return render_template('404.html'), 404
# @app.errorhandler(Exception)
# def internal_error(error):
#     return render_template('500.html'), 500

if __name__ == "__main__":
    app.run()



