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
from Forms import Question, Response
from datapipeline import *
app = Flask(__name__)
app.secret_key = "sadbiscuit"
app.config["PRODUCT_IMAGE_UPLOAD"] = "static/product_images"
app.config["PROFILE_IMAGE_UPLOAD"] = "static/profile_pics"
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
    if session.get('forced_logout')==True:
        session['forced_logout']=False
        return redirect(url_for('logout'))

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
                session['forced_logout']=True
                session['logged_in']=False
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
    return render_template('home_page.html' ,product_list = Products,women = womenlist,men = menlist,child = childernlist )



#currently not working ui not done yet whatsapp me before touching this  
@app.route("/product/<productid>")
def product_page(productid):
    get_product = get_product_by_id(productid)
    seller = get_user(get_product.get_seller_id())
    return render_template('productdetails.html',product = get_product,sellerinfo = seller.get_username() )

# only be able to access if session['logged_in']==True
@app.route("/wishlist")
def wish_list():
    wishlist = fetch_wishlist(session.get('user_id'))
    return render_template('wishlist.html',wishlist = wishlist)

@app.route("/addwishlist/<productid>")
def add_wish_list(productid):
    if session.get('logged_in') == True:
        current_wishlist=fetch_wishlist_id(session.get('user_id'))
        if productid in current_wishlist:
            flash('product already in wishlist')
            return redirect(url_for('landing_page'))
        else:
            pass
            update_wishlist(session.get('user_id'),productid)
            return redirect(url_for('landing_page'))
    else:
        return redirect(url_for('loginUser'))


@app.route("/delwishlist/<productid>")
def del_wish_list(productid):
    delete_wishlist(session.get('user_id'),productid)
    return redirect(url_for('wish_list'))

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
    if session.get('logged_in')==True:
        if session.get('role') == 'S':
            ownp= get_usr_owned_p(session.get('user_id'))
            all_profit = api_all_profit(ownp)
            orderlist=create_seller_order_list(session.get('user_id'))
            pending_order=pending_order_check(orderlist)
        else:
            all_profit = 0
            pending_order=0
        return render_template('chart.html',all_profit=all_profit,pending_order=pending_order)
    else:
        return redirect(url_for('landing_page'))
@app.route("/data/<d_type>")
def datapipe(d_type):
    if session.get('role') == 'S':
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
        elif d_type == 'bar_all':
            chart_data = get_all_qty_data(ownp)
            return jsonify(chart_data)
        else:
             return None
    else:
        return None


# @app.route("/apitest")
# def datatest():
#     ownp = ['a9ee20758e2647f69d3bbf92066f3d31']
#     if request.args.get('type') == 'ALL':
#         apidata = api_get_all(ownp,request.args.get('datetype'),request.args.get('date'))
#         if apidata is not None:
#             profit = []
#             dtime = []
#             for orders in apidata:
#                 profit.append(orders.get_o_profit())
#                 dtime.append(orders.get_timestamp_as_datetime().strftime("%m/%d/%Y %H:%M:%S"))
#             return jsonify({"profit":profit},{"datetime":dtime})
#         else:
#             return jsonify({"profit":None},{"datetime":None})

#     else:
#         return jsonify({"profit":None},{"datetime":None})




    # apidata = api_func()
    # profit = apidata[0]
    # dtime = apidata[1]
    # return jsonify({"profit":profit},{"datetime":dtime})
@app.route("/user_logs")
def userdashboard_logs():
    db = shelve.open('database/logs_database/logs.db', 'r')
    userslogList = []
    for user in db:
        try:
            user_log = get_user_log_by_id(user)
            userslogList.append(user_log)
        except AttributeError:
            pass
    if userslogList is not None:
        return render_template('admin_logs_page.html',user_log_list = userslogList)
    else:
        return render_template('admin_logs_page.html')


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
             
             filename = secure_filename(i.filename)
             if os.path.isfile('static/product_images/{}'.format(filename)) == True:
                 filename = filename.split('.')
                 newfilename = str(uuid.uuid4()) + '.' + filename[1]
                 i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],newfilename))
                 filenames.append(newfilename)
             else:
                i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
                filenames.append(filename)
        if Product_Form.product_Discount.data < Product_Form.product_Selling_Price.data:
            new_product = Add_New_Products(session.get('user_id'),Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames) 
            flash('Product successfully created')
            return redirect(url_for('dashboard_products')) 
        else:
            error = 'Discount amount cannot be greater than selling price'
            return render_template('productcreateform.html',form =Product_Form ,ftype = 'create',error = error)
             
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
        if Product_Form.product_Discount.data < Product_Form.product_Selling_Price.data:
            product_pics = Product_Form.product_images.data
            check_if_empty = [i.filename for i in product_pics]
            if '' in check_if_empty:
                Edit_Products(session.get('user_id'),productid,Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,original_product.get_product_images())
            else:
                for i in product_pics:
                    #TODO 
                    filename = secure_filename(i.filename)
                    if os.path.isfile('static/product_images/{}'.format(filename)) == True:
                        filename = filename.split('.')
                        newfilename = str(uuid.uuid4()) + '.' + filename[1]
                        i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],newfilename))
                        filenames.append(newfilename)
                    else:
                        i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
                        filenames.append(filename)
                #pass form data to Edit_Products function in model.py
                Edit_Products(session.get('user_id'),productid,Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)
            flash('Product successfully updated')
            return redirect(url_for('dashboard_products')) 
        else:
            error = 'Discount amount cannot be greater than selling price'
            return render_template('productcreateform.html',form =Product_Form,ftype ='update',error = error)

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

@app.route("/review/<productid_track>",methods = ['POST','GET'])
def review(productid_track):
    productid_track = productid_track.split('-')
    productid = productid_track[0]
    trackingid = productid_track[1]
    Review_form = review_form(request.form)
    if request.method == 'POST'  and Review_form.validate():
        add_review(session.get('user_id'),session.get('name'),productid,int(Review_form.rating.data),Review_form.review_text.data)
        review_status_update(session.get('user_id'),trackingid,'Yes')
        return redirect(url_for('delivery_history'))
    return render_template('review_form.html',form = Review_form)
 
 

#User Management
#sign up user
@app.route('/signup', methods=['GET', 'POST'])

def signupUser():
    if session.get('logged_in')==True:
        return redirect(url_for("landing_page"))
    createUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and createUserForm.validate():
        email = request.form['email']
        username = request.form['username']
        db = shelve.open('database/user_database/user.db', 'r')
        for user in db:
                user=db[user]
                if user.get_user_email()==email:
                    error = 'This email is in use, please enter another email.'
                    return render_template('Signup.html', form=createUserForm, error=error)
                if user.get_username()==username:
                    usernameerror = 'This username is in use, please enter another username.'
                    return render_template('Signup.html', form=createUserForm, usernameerror=usernameerror)
        db.close()
        password = request.form['password']
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
    user_logging(user.get_user_id(),'CREATE',user,user.get_username())
    db.close()
    flash('Your account has been verified')
    return redirect(url_for("landing_page"))

@app.route('/retrieveUsers')
def retrieveUsers():
    if session.get('logged_in')==True and session.get('role')=="A":
        db = shelve.open('database/user_database/user.db', 'r')
        usersList = []
        for user in db:
            user=db[user]
            usersList.append(user)
        db.close()

        return render_template('retrieveUsers.html',usersList=usersList, count=len(usersList))
    else:
        return redirect(url_for("landing_page"))

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

@app.route('/create_newpassword_profile/<id>',methods=['GET','POST'])
def create_newpassword_profile(id):
    getPasswordForm=PasswordReset(request.form)
    if request.method == 'POST' and getPasswordForm.validate():
        userid=id
        db = shelve.open('database/user_database/user.db', 'w')
        user=db[userid]
        pw=request.form['password']
        user.set_user_pw(pw)
        db[userid]=user
        db.close()
        flash('Your password has changed successfully')
        return redirect(url_for("profile"))
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
                        user_logging(user.get_user_id(),'LOGIN',user,user.get_username())
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
    try:
        db = shelve.open('database/user_database/user.db', 'r')
        userid=session['user_id']
        user=db[userid]
        user_logging(user.get_user_id(),'LOGOUT',user,user.get_username())
        db.close()
    except:
        pass
    session.clear()
    return redirect(url_for('landing_page'))



@app.route('/updateUser/<id>', methods=['GET', 'POST'])
def updateUser(id):
    updateUserForm = CreateUpdateForm(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        username = request.form['username']
        email = request.form['email']
        db = shelve.open("database/user_database/user.db", "w")
        oguser = db[id]
        for user in db:
            user=db[user]
            if user.get_user_email()==email:
                if oguser.get_user_email()==email:
                    pass
                else:
                    error = 'This email is in use, please enter another email.'
                    return render_template('updateUser.html', form=updateUserForm, error=error)
            if user.get_username()==username:
                if oguser.get_username()==username:
                    pass
                else:
                    usernameerror = 'This username is in use, please enter another username.'
                    return render_template('updateUser.html', form=updateUserForm, usernameerror=usernameerror)
        user = db[id]
        user.set_user_email(updateUserForm.email.data)
        user.set_username(updateUserForm.username.data)
        user.set_user_firstname(updateUserForm.firstname.data)
        user.set_user_lastname(updateUserForm.lastname.data)
        user.set_user_role(updateUserForm.role.data)
        db[id]=user
        user_logging(user.get_user_id(),'EDIT',user,user.get_username())

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


@app.route('/updateprofile/<id>', methods=['GET', 'POST'])
def updateprofile(id):
    updateprofileForm = CreateProfileUpdateForm(request.form)
    if request.method == 'POST' and updateprofileForm.validate():
        profile_pic = CreateProfileUpdateForm(request.files)
        username = request.form['username']
        email=request.form['email']
        db = shelve.open("database/user_database/user.db", "w")
        oguser=db[id]
        for user in db:
            user=db[user]
            if user.get_user_email()==email:
                if oguser.get_user_email()==email:
                    pass
                else:
                    error = 'This email is in use, please enter another email.'
                    return render_template('updateprofile.html', form=updateprofileForm, error=error)
            if user.get_username()==username:
                if oguser.get_username()==username:
                    pass
                else:
                    usernameerror = 'This username is in use, please enter another username.'
                    return render_template('updateprofile.html', form=updateprofileForm, usernameerror=usernameerror)
        user = db[id]
        user.set_user_email(updateprofileForm.email.data)
        user.set_username(updateprofileForm.username.data)
        user.set_user_firstname(updateprofileForm.firstname.data)
        user.set_user_lastname(updateprofileForm.lastname.data)
        profile_pic = profile_pic.profile_picture.data
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config["PROFILE_IMAGE_UPLOAD"],secure_filename(profile_pic.filename)))
            if user.get_user_profile_picture()!="80-804695_profile-picture-default-png.png":
                old_profile_pic=(os.path.join(app.config['PROFILE_IMAGE_UPLOAD'],user.get_user_profile_picture()))
                if os.path.exists(old_profile_pic)==True:
                    os.remove(old_profile_pic)
            user.set_user_profile_picture(filename)


        db[id]=user
        session['profile_picture']=user.get_user_profile_picture()
        user_logging(user.get_user_id(),'EDIT',user,user.get_username())
        db.close()
        return redirect(url_for("profile"))
    else:
        db = shelve.open('database/user_database/user.db', 'r')
        user = db[id]
        updateprofileForm.email.data = user.get_user_email()
        updateprofileForm.username.data = user.get_username()
        updateprofileForm.firstname.data = user.get_user_firstname()
        updateprofileForm.lastname.data = user.get_user_lastname()
        updateprofileForm.profile_picture.data = user.get_user_profile_picture()
        db.close()
        return render_template('updateprofile.html',form=updateprofileForm)


@app.route('/deleteUser/<id>', methods=['POST'])
def deleteUser(id):
    db = shelve.open('database/user_database/user.db', 'r')
    user=db[id]
    username=user.get_username()
    if user.get_user_role()=="S":
        delete_all_user_product(id)
    deleted_user=db.pop(id)
    user_logging(user.get_user_id(),'DELETE',deleted_user,username)
    db.close()
    return redirect(url_for('retrieveUsers'))


#adding  product to cart 
@app.route('/profile')
def profile():
    if session.get('logged_in') == True:
        db = shelve.open('database/user_database/user.db', 'r')
        usersList = []
        for user in db:
            user=db[user]
            usersList.append(user)
        db.close()

        return render_template('profile.html',usersList=usersList, count=len(usersList))
    else:
        return redirect(url_for('landing_page'))


#Order Management
#adding product to cart
@app.route('/add_to_cart/<productid>/<int:productqty>')
def Add_to_cart(productid,productqty):
    if session.get('logged_in') == True:
        userid=session.get('user_id')
        userrole=session.get('role')
        if userrole=="A":
            return redirect(url_for('landing_page'))
        db=shelve.open('database/user_database/user.db','r')
        if db[userid].get_user_role()=="S":
            return redirect(url_for('landing_page'))
        db.close()
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
        flash("Product added to the Cart")
        return redirect(url_for('landing_page'))
    else:
        return redirect(url_for('loginUser'))

@app.route('/cart')
def cart():
    if session.get('logged_in') == True:
        #initalise a empty list for product objects in varible productincart
        userid=session.get('user_id')
        userrole=session.get('role')
        if userrole=="A":
            return redirect(url_for('landing_page'))
        db=shelve.open('database/user_database/user.db','r')
        if db[userid].get_user_role()=="S":
            return redirect(url_for('landing_page'))
        db.close()
        productincart = []
        db=shelve.open('database/order_database/cart.db','c')
        # if user record exist fetch it from cart db and put it in varible usercart
        if session.get('user_id')in db:
            usercart=db.get(session.get('user_id'))
            #retrive product object from product db using the product id stored in usercart dict
            for item in usercart.keys():
                productincart.append(get_product_by_id(item))
        else:
            #if user record does not exist , usercart is initalise as a empty dict
            # and save empty dict to db so if user open cart without adding items there will be no error
            usercart={}
        db.close()
        total_price=0
        total_discount=0
        Grand_total=0
        for i in productincart:
            price=i.get_product_price()*usercart[i.get_product_id()]
            discount=i.get_product_discount()*usercart[i.get_product_id()]
            grand=i.get_discounted_price()*usercart[i.get_product_id()]
            total_price+=price
            total_discount+=discount
            Grand_total+=grand
        return render_template('Add_To_Cart.html',usercart = usercart,productincart = productincart,total_price=total_price,total_discount=total_discount,Grand_total=Grand_total)
    else:
        return redirect(url_for('loginUser'))

@app.route('/deletecart/<cartproductid>',methods = ['POST'])
#take in post request from the route and the product id of the item to be deleted
def deletecart(cartproductid):
    try:
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
        db.close()
    except IOError:
        print("db file not found")
    except:
        print("Unknown error")
    return redirect(url_for('cart'))

@app.route('/Updatecart/<cartproductid>',methods=['POST','GET'])
def Updatecart(cartproductid):
    updateForm=updateorderForm(request.form)
    if request.method=="POST" and updateForm.validate():
        if updateForm.orderqty.data>=1:
            Updateqty(updateForm.orderqty.data,session.get('user_id'),cartproductid)
            return redirect(url_for('cart'))
        else:
            flash('Invalid quantity')
            return render_template('Updateorderqty.html',form=updateForm)
    return render_template('Updateorderqty.html',form=updateForm)


@app.route('/Deliverydetails', methods=['GET','POST']) #address,country,city,state,zip,userid
def Deliverydetails():
    delivery_form= DeliveryForm(request.form)
    if request.method == "POST" and delivery_form.validate():
            add_delivery_info(delivery_form.address.data,delivery_form.country.data,delivery_form.city.data,delivery_form.state.data,delivery_form.zip.data,session.get('user_id'))
            return redirect(url_for('paymentdetails'))
    return render_template('delivery_details.html',form=delivery_form)


@app.route('/Paymentdetails', methods=['GET','POST'])
def paymentdetails():
    payment1_form=Payment_Form(request.form)
    if request.method == "POST" and payment1_form.validate():
            # payment_confirmation(payment1_form.cardholder.data,payment1_form.cardno.data,payment1_form.expiry.data,payment1_form.cvc.data,session.get('user_id'))
            return redirect(url_for('confirmation'))
    return render_template('Payment.html',form=payment1_form)


@app.route('/orderconfirm',methods=['GET'])
def confirmation():
    productincart=[]
    db=shelve.open('database/order_database/cart.db','r')
    if session.get('user_id')in db:
        usercart=db.get(session.get('user_id'))
        print(usercart)
        for item in usercart:
            productincart.append(get_product_by_id(item))
    db.close()
    total_price=0
    total_discount=0
    Grand_total=0
    for i in productincart:
        price=i.get_product_price()*usercart[i.get_product_id()]
        discount=i.get_product_discount()*usercart[i.get_product_id()]
        grand=i.get_discounted_price()*usercart[i.get_product_id()]
        total_price+=price
        total_discount+=discount
        Grand_total+=grand
    db=shelve.open('database/order_database/order.db','c')
    Neworder = Order(session.get('user_id'),usercart,session.get('name'),Grand_total)
    db[Neworder.get_orderId()]=Neworder
    db.close()
    db=shelve.open('database/user_database/user.db','r')
    if session.get('user_id') in db:
        usr=db.get(session.get('user_id'))
        add = usr.get_user_address()
        full_address=add["address"]+ " " + add["country"]+ " "+ add["city"]+ " "+ add["state"]+" "+ add["zip"]
        print(full_address)
    db.close()
    db=shelve.open('database/order_database/cart.db')
    db.pop(session.get('user_id'))
    db.close()
    # Pass to the delivery management
    separating_orders(session.get('user_id'),usercart,Neworder.get_timestamp_as_datetime(),full_address)
    order_log_preprocess(session.get('user_id'),Neworder)
    return render_template('order_confirmation.html',usercart = usercart,productincart = productincart, total_price=total_price,total_discount=total_discount,Grand_total=Grand_total)

@app.route('/Myorder')
def order():
    #list of all the product objects in customer order 
    productinorder = {}
    userorder_list = []
    db=shelve.open('database/order_database/order.db','c')
    userorder = get_buyer_orders(session.get('user_id'))
    for order in userorder:
        userorder_list.append(order.get_cart_list())
        for item in order.get_cart_list():
            product_obj = get_product_by_id(item)
            if product_obj.get_product_id() not in productinorder:
                productinorder[product_obj.get_product_id()] = product_obj
    db.close()
    # if session.get('user_id')in db:
    #     userorder=db.get(session.get('user_id'))
    #     for item in userorder.get_cart_list():
    #         productinorder.append(get_product_by_id(item))
    # db.close()
    return render_template('MyOrder.html',orders = userorder_list,productinorder=productinorder)

@app.route('/SellerOrder')
def seller_order():
    if session.get('logged_in')==True:
        userid=session.get('user_id')
        db=shelve.open('database/user_database/user.db','r')
        if db[userid].get_user_role()!="S":
            return redirect(url_for('order'))
        db.close()
        productinorder = {}
        seller_order = []
        order=get_seller_orders(session.get('user_id'))
        for i in order:
            # seller_order.append(i.get_cart_list())
            for n in i.get_cart_list():
                if n != 'orderid' and n != 'buyerid':
                    print(n)
                    order_obj=get_product_by_id(n)
                    if order_obj.get_product_id() not in productinorder:
                        productinorder[order_obj.get_product_id()]=order_obj
        return render_template('Seller_order_list.html',orders=order,productinorder=productinorder)
    else:
        return redirect(url_for("landing_page"))

#delivery management
@app.route('/SellerDelivery')
def seller_deliverylist():
    userid=session.get('user_id')
    db=shelve.open('database/user_database/user.db','r')
    if db[userid].get_user_role()!="S":
        return redirect(url_for('buyer_deliverylist'))
    db.close()
    delivery_list=create_seller_order_list(session.get('user_id'))
    return render_template('seller_delivery_status.html',delivery_list=delivery_list)


@app.route('/SellerDeliveryUpdate/<orderid>',methods=['POST','GET'])
def delivery_status_update(orderid):
    updatedstatusform= NewStatus(request.form)
    #db=shelve.open('database/delivery_database/delivery.db', 'c')
    sellerorderlist=create_seller_order_list(session.get('user_id'))
    for i in sellerorderlist:
        if i.get_individual_orderid()==orderid:
            orderobj=i
    #db.close()
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

#to get the detailed details of order
@app.route('/BuyerDeliveryDetails/<orderid>')
def buyer_deliverydetails(orderid):
    #try:
    db=shelve.open('database/delivery_database/delivery.db', 'c')
    buyerorderlist=create_buyer_order_list(session.get('user_id'))
    for i in buyerorderlist:
        if i.get_individual_orderid()==orderid:
            orderobj=i
    db.close()
    rstatobj=recent_courier_stat(orderid)
    if rstatobj != False:
        status=rstatobj.get_status()
        statusdate=rstatobj.get_status_date()
        statusnote=rstatobj.get_delivery_notes()
    else:
        status="None"
        statusnote="None"
        statusdate="None"
    return render_template('buyer_order_details2.html',individual_order=orderobj,status=status,statusdate=statusdate,statusnote=statusnote)
    #except IOError:
    #    print("db does not exist")
    #except:
    #    print("an unknown error occurred")

@app.route('/DeliveryHistory')
def delivery_history():
    userid=session.get('user_id')
    userrole=session.get('role')
    if userrole=='B':
        db=shelve.open('database/delivery_database/delivery.db','c')
        if userid in db:
            history=buyer_history_list(userid)
        else:
            history=[]
        db.close()
        return render_template('buyer_delivery_history.html',history=history)

    history=seller_history_list(userid)
    return render_template('seller_delivery_history.html',history=history)

@app.route('/DeletingDelivery/<orderid>/<userid>')
def deleting_delivery(orderid,userid):
    #deleting_delivery(userid,orderid)
    try:
       db=shelve.open('database/delivery_database/delivery.db','r')
       biglist=db[userid]
       for i in biglist:
           for n in i:
               if n.get_individual_orderid()==orderid:
                   i.remove(n)
       db[userid]=biglist
       db.close()
    except IOError:
        print("db not found")
    except:
        print("an unknown error occurred")
    return redirect(url_for('buyer_deliverylist'))

#redo this part
@app.route('/DeliveryReceived/<trackingid>')
def received_delivery(trackingid):
    userid=session.get('user_id')
    userrole=session.get('role')
    if userrole=='B':
        status_update(trackingid,userid,"Order Received")
        #deliverylist=create_buyer_order_list(userid)
        db=shelve.open('database/delivery_database/delivery.db','c')
        userlist=db[userid]
        for i in userlist:
            for n in i:
                if n.get_individual_orderid()==trackingid:
                    n.set_buyer_checker('Yes')
                    deldate=datetime.date(datetime.today())
                    n.set_delivery_received_date(deldate)
        db[userid]=userlist
        db.close()
        return redirect(url_for('buyer_deliverylist'))
    else:
        db=shelve.open('database/delivery_database/delivery.db','c')
        for i in db:
            for j in db[i]:
                for k in j:
                    if k.get_individual_orderid()==trackingid:
                        userid=i
        biglist=db[userid]
        for i in biglist:
            for n in i:
                if n.get_individual_orderid()==trackingid:
                    n.set_seller_checker('Yes')
                    if n.get_deliverystat()=="Pending":
                        n.set_delivery_status("--")
        db[userid]=biglist
        db.close()
        return redirect(url_for('seller_deliverylist'))
    #return redirect(url_for('review',productid=productid))


@app.route('/SellerDeliveryReceived/<trackingid>/<buyerid>')
def seller_acknowledge(trackingid,buyerid):
    status_update(trackingid,buyerid,"Order Received (Acknowleged)")
    return redirect(url_for('seller_deliverylist'))

@app.route('/AdminvsBSCheck')
def checking_role():
    userid=session.get('user_id')
    userrole=session.get('role')
    if userrole=="A":
        return redirect(url_for('CarrierUpdate'))
    else:
        return redirect(url_for('Carrierbuyer'))

@app.route('/CarrierBuyer', methods=['GET','POST'])
def Carrierbuyer():
    carrierbuyer=CarrierBuyer(request.form)
    buttoncheck='No'
    if request.method=='POST' and carrierbuyer.validate():
        orderid=carrierbuyer.orderid.data
        ordercheck=checking_id(orderid)
        if ordercheck==True:
            db=shelve.open('database/delivery_database/carrier.db','c')
            statuslist=db[orderid]
            db.close()
            dobj=delivery_object(orderid)
            return render_template('carrieruser_details.html',statuslist=statuslist,orderid=orderid,deliverObj=dobj)
        error='Woops, seems like ID has not been added. Try Again'
        return render_template('carrieruser.html',form=carrierbuyer,error=error,buttoncheck=buttoncheck)
    else:
        return render_template('carrieruser.html',form=carrierbuyer,buttoncheck=buttoncheck)

@app.route('/CarrierBuyerDash',methods=['GET','POST'])
def carrierbuyerdash():
    carrierbuyer=CarrierBuyer(request.form)
    buttoncheck='Yes'
    if request.method=='POST' and carrierbuyer.validate():
        orderid=carrierbuyer.orderid.data
        ordercheck=checking_id(orderid)
        if ordercheck==True:
            db=shelve.open('database/delivery_database/carrier.db','c')
            statuslist=db[orderid]
            db.close()
            dobj=delivery_object(orderid)
            return render_template('carrieruser_details.html',statuslist=statuslist,orderid=orderid,deliverObj=dobj)
        error='Woops, seems like ID has not been added. Try Again'
        return render_template('carrieruser.html',form=carrierbuyer,error=error,buttoncheck=buttoncheck)
    else:
        return render_template('carrieruser.html',form=carrierbuyer,buttoncheck=buttoncheck)

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
                for j in n:
                    if j.get_individual_orderid()==orderid:
                        checker=True
                        address=j.get_address()
        db.close()
        if checker==True:
            carrierobj_and_db(orderid,updatedate,country,status,deliverynotes,address)
            #return render_template('testing2.html',statuslist=statuslist,orderid=orderid)
            return redirect(url_for('CarrierUpdateTable',trackingid=orderid))
        else:
            error="Tracking ID not found"
            return render_template('carrier_update.html',form=carrierupdateform, error=error)
    return render_template('carrier_update.html',form=carrierupdateform)



@app.route('/RedirectingCarrierUpdate/<trackingid>')
def CarrierUpdateTable(trackingid):
    #try:
    db=shelve.open('database/delivery_database/carrier.db','c')
    if trackingid in db:
        statuslist=db[trackingid]
    db.close()
    dobj=delivery_object(trackingid)
    return render_template('testing2.html',statuslist=statuslist,orderid=trackingid,deliverObj=dobj)
    #except IOError:
        #print("db not found")
    #except:
        #print("an unknown error has occurred")

@app.route('/DeletingCarrierUpdate/<updateid>/<trackingid>')
def deleting_update(updateid,trackingid):
    try:
        db=shelve.open('database/delivery_database/carrier.db','c')
        updatelist=db[trackingid]
        for i in updatelist:
            if i.get_status_id()==updateid:
                updatelist.remove(i)
        db[trackingid]=updatelist
        db.close()

    except IOError:
        print("db not found")
    except:
        print("an unknown error has occurred")
    # return render_template('testing2.html',statuslist=updatelist,orderid=trackingid)
    return redirect(url_for('CarrierUpdateTable', trackingid=trackingid))

@app.route('/EditUpdate/<trackingid>/<statusid>',methods=['GET','POST'])
def UpdatingStatus(trackingid,statusid):
    statusupdateform=CarrierUpdateForm(request.form)
    if request.method=='POST' and statusupdateform.validate():
        country=statusupdateform.country.data
        status=statusupdateform.status.data
        deliverynotes=statusupdateform.deliverynotes.data
        editing_status(trackingid,status,deliverynotes,country,statusid)
        return redirect(url_for('CarrierUpdateTable', trackingid=trackingid))
    else:
        #try:
        db=shelve.open('database/delivery_database/carrier.db','c')
        listobj=db[trackingid]
        for i in listobj:
            if i.get_status_id()==statusid:
                statusobj=i
        db.close()
        return render_template('carriereditstatus.html',statusinfo=statusobj,form=statusupdateform,trackingid=trackingid)
        #except IOError:
        #    print("db not found")
        #except:
        #    print("an unknown error has occurred")


#FAQ Display
@app.route('/FAQ')
def FAQ():
    #user for rx forum
    user=shelve.open('database/user_database/user.db')
    users={}
    for i in user.values():
        users[i.get_user_id()]=i.get_user_fullname()
    user.close()


    role="NU"
    if session.get('logged_in')== True:
        if session.get('role')=='A':
            role="A" 
        else:
            role="U"   
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
        print("The Second Database has not been found")
    return render_template('FAQ.html', Gold=Gold, FaQ=FaQ , AcI=AcI,CoI=CoI,role=role,users=users)


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
        faq_logging(session.get('user_id'),'Forum','CREATE',new_question.get_msgid(),new_question)
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
        faq_logging(session.get('user_id'),'Forum','REPLY',Respondents.get_ansid(),Respondents)
        RespondtoQns(Respondents.get_ansid(),id)
        return redirect(url_for('displayQns',id=id))
    return render_template('Response.html',form=Reply)

@app.route('/displayQns/<id>')
def displayQns(id):
    #user for rx forum
    user=shelve.open('database/user_database/user.db','r')
    users={}
    for i in user.values():
        users[i.get_user_id()]=[i.get_user_fullname(), i.get_user_profile_picture()]
    user.close()

    role="NU"
    uid=session.get('user_id')
    if session.get('logged_in')== True:
        if session.get('role')=='A':
            role="A" 
        else:
            role="U"   
    question = get_question_by_id(id)
    AnswerList=get_answer_by_id(question.get_ans_list())
    return render_template('displayQns.html',question = question, AnswerList=AnswerList, role=role, uid=uid,users=users)

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
        faq_logging(session.get('user_id'),'Forum','EDIT',Qns.get_msgid(),Qns)
        return redirect(url_for('FAQ'))
    else:
        db= shelve.open('database/forum_database/FAQQ.db','r')
        Qns= db.get(id)
        db.close()
        updateQns.mtitle.data= Qns.getmtitle()
        updateQns.mbody.data=Qns.getmbody()
        return render_template('updateqns.html',form=updateQns)

#Transactions
@app.route('/addFAQueryFaQ',methods=["GET","POST"])
def addFAQueryF():
    Drei=FAQd(request.form)
    if request.method=="POST" and Drei.validate():

        A=FAQm(Drei.question.data,Drei.answer.data)
        try:
            Three=shelve.open("database/forum_database/FAQDisplay.db","c")
            Three[A.getid()] = A
            
        except IOError:
            print("ooopsie")
        Three.close()
        faq_logging(session.get('user_id'),'Transactions','CREATE',A.getid(),A)
        return redirect(url_for('FAQ'))
    return render_template('faqopening1.html',form=Drei)
#Account Issues
@app.route('/addFAQueryAcI',methods=["GET","POST"])
def addFAQueryAcI():
    Vier=FAQd(request.form)
    if request.method=="POST" and Vier.validate():
        AcI=Account_Issues(Vier.question.data,Vier.answer.data)
        try:
            Four=shelve.open("database/forum_database/FAQDisplay.db","c")
            Four[AcI.getid()] = AcI
            
        except IOError:
            print("ooopsie")
        Four.close()
        faq_logging(session.get('user_id'),'Account Issues','CREATE',AcI.getid(),AcI)
        return redirect(url_for('FAQ'))
    return render_template('faqopening1.html',form=Vier)
#Contact Us
@app.route('/addFAQueryCoI',methods=["GET","POST"])
def addFAQueryCoI():
    Fuenf=FAQd(request.form)
    if request.method=="POST" and Fuenf.validate():

        CoI=Contact(Fuenf.question.data,Fuenf.answer.data)
        try:
            Five=shelve.open("database/forum_database/FAQDisplay.db","c")
            Five[CoI.getid()] = CoI
        except IOError:
            print("ooopsie")
        Five.close()
        faq_logging(session.get('user_id'),'Contact Us','CREATE',CoI.getid(),CoI)
        return redirect(url_for('FAQ'))
    return render_template('faqopening1.html',form=Fuenf)

#update Qns in FAQ only seen by admin
@app.route('/updateFAQueryF/<id>',methods=["GET","POST"])
def updateFAQueryF(id):
    if session.get('logged_in') and session.get('role')=="A":
        updateFAQueryF=FAQd(request.form)
        updateFAQueryF=FAQd(request.form)
        if request.method =='POST' and updateFAQueryF.validate():
            db=shelve.open('database/forum_database/FAQDisplay.db','w')
            Fa= db.get(id)
            Fa.setquestion(updateFAQueryF.question.data)
            Fa.setanswer(updateFAQueryF.answer.data)

            db[id]= Fa
            db.close()
        
            faq_logging(session.get('user_id'),'frequently asked questions','EDIT',Fa.getid(),Fa)
            return redirect(url_for('FAQ'))

        else:
            db= shelve.open('database/forum_database/FAQDisplay.db','r')
            Qns= db.get(id)
            db.close()

            updateFAQueryF.question.data= Qns.getquestion()
            updateFAQueryF.answer.data=Qns.getanswer()
            return render_template('faqopening2.html',form=updateFAQueryF)

#update Qns in FAQ only see button
@app.route('/updateFAQueryA/<id>',methods=["GET","POST"])
def updateFAQueryA(id):
    if session.get('logged_in')==True and session.get('role')=="A":
        updateFAQueryA=FAQd(request.form)
        if request.method =='POST' and updateFAQueryA.validate():
            db=shelve.open('database/forum_database/FAQDisplay.db','w')
            Fa= db.get(id)
            Fa.setquestion(updateFAQueryA.question.data)
            Fa.setanswer(updateFAQueryA.answer.data)

            db[id]= Fa
            db.close()
            faq_logging(session.get('user_id'),'Account Issues','EDIT',Fa.getid(),Fa)
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
    if session.get('logged_in')==True and session.get('role')=="A":
        updateFAQueryC=FAQd(request.form)
        if request.method =='POST' and updateFAQueryC.validate():
            db=shelve.open('database/forum_database/FAQDisplay.db','w')
            Fa= db.get(id)
            Fa.setquestion(updateFAQueryC.question.data)
            Fa.setanswer(updateFAQueryC.answer.data)

            db[id]= Fa
            db.close()
            faq_logging(session.get('user_id'),'Contact Us','EDIT',Fa.getid(),Fa)
            return redirect(url_for('FAQ'))

        else:
            db= shelve.open('database/forum_database/FAQDisplay.db','r')
            Qns= db.get(id)
            db.close()

            updateFAQueryC.question.data= Qns.getquestion()
            updateFAQueryC.answer.data=Qns.getanswer()
            return render_template('faqopening2.html',form=updateFAQueryC)
#Delete FAQ Qns
@app.route('/deleteQns/<id>')
def deleteQns(id):
    if session.get('logged_in')==True and session.get('role')=="A":
        Ace=shelve.open('database/forum_database/FAQDisplay.db','w')
        deleted_faq = Ace.pop(id)
        Ace.close()
        if isinstance(deleted_faq,FAQm):
            faq_type= "frequently asked questions"
        elif isinstance(deleted_faq,Account_Issues):
            faq_type="account issues"
        else:
            faq_type="contact us"
        faq_logging(session.get('user_id'),faq_type,'DELETE',deleted_faq.getid(),deleted_faq)
        return redirect(url_for('FAQ'))
#Delete Forum Qns
@app.route('/deleteForumQns/<id>')
def deleteForumQns(id):
    if session.get('logged_in')==True:
        Ace=shelve.open('database/forum_database/FAQQ.db','w')
        ri= Ace[id]

        for i in ri.get_ans_list():
            f=Ace.pop(i)
            faq_logging(session.get('user_id'),'Forum','DELETE',f.get_ansid(),f)

        a=Ace.pop(id)
        Ace.close()
        faq_logging(session.get('user_id'),'Forum','DELETE',a.get_msgid(),a)
    return redirect(url_for('FAQ'))
#Show FAQ Log
@app.route('/FAQLOG')
def FAQLOG():
    if session.get('logged_in')==True and session.get('role')=="A":
        db=shelve.open("database/logs_database/logs.db",'r')
        logs=[]
        for a in db.values():
            if len(a.get_faq_log_list()) > 0:
                for i in a.get_faq_log_list():
                    logs.append(i)

        db.close()
        return render_template('displayfaqlogs.html',log=logs)        
    else:
        return redirect(url_for('FAQ'))
# @app.errorhandler(404)
# def not_found_error(error):  
#     return render_template('404.html'), 404
# @app.errorhandler(Exception)
# def internal_error(error):
#     return render_template('500.html'), 500

if __name__ == "__main__":
    app.run()


