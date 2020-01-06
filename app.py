import shelve
from flask import *
import os
from Forms import Create_Product_Form, CreateLoginForm, CreateUserForm, CreateUpdateForm,Edit_Product_Form
from werkzeug.datastructures import CombinedMultiDict,FileStorage
from werkzeug import secure_filename
from model import *
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from datapipeline import *
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer

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
s= URLSafeSerializer(app.secret_key)
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
    return render_template('home_page.html' ,product_list = Products )

@app.route('/cart/<productid>/<int:productqty>')
def test_route(productid,productqty):
        var = cartItem(productid,productqty)
        var.to_json
        cart = session["cart"]=[]
        cart.append(var)
        print(cart)
        return jsonify({'id':'test'},{'qty':'test'})

#currently not working ui not done yet whatsapp me before touching this  
@app.route("/product/<productid>")
def product_page(productid):
    get_product = get_product_by_id(productid)
    return render_template('productdetails.html',product = get_product)

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

# @app.route("/data")
# def datapipe():
#     pdata = test_func()
#     profit = pdata[0]
#     dtime = pdata[1]
    
#     return jsonify({"profit":profit},{"datetime":dtime})

@app.route("/apitest")
def datatest():
    ownp = ['d97db4c0ab7a4e75935fd6bb7a8e8f51','7ee8e6589fa24898af240be7ff546f14','ba2f9310e9e64230890298ffe4f20401']
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
    user_id = session.get('user_id')
    return render_template('staff_logs_page.html',product_log_list = product_log,userid = user_id )

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
             i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
             filenames.append(filename)
        new_product = Add_New_Products(session.get('user_id'),Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)  
        return redirect(url_for('dashboard_products'))      
    return render_template('productcreateform.html',form =Product_Form )

    
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
                 filename = secure_filename(i.filename)
                 i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
                 filenames.append(filename)
            #pass form data to Edit_Products function in model.py
            Edit_Products(session.get('user_id'),productid,Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)
        return redirect(url_for('dashboard_products')) 
    else:
        Product_Form.product_name.data = original_product.get_product_name()
        Product_Form.product_Quantity.data = original_product.get_product_current_qty()
        Product_Form.product_Description.data = original_product.get_product_desc()
        Product_Form.product_Selling_Price.data = original_product.get_product_price()
        Product_Form.product_Discount.data = original_product.get_product_discount()
        Product_Form.product_catergory.data = original_product.get_product_catergory()
        Product_Form.product_images.data = original_product.get_product_images()
    return render_template('productcreateform.html',form =Product_Form)

#take in product id and delete product from shelve  
@app.route("/delete_products/<productid>",methods=['POST'])
def delete_products(productid):
    delete_product_by_id(productid,session.get('user_id'))
    return redirect(url_for('dashboard_products'))



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
    user=s.loads(token,salt='email-confirm')
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

#login user, session['logged_in']==True here
@app.route('/login', methods=('GET', 'POST'))

def loginUser():
    if session.get('logged_in')==True:
        return redirect(url_for("landing_page"))
    else:
        createLoginForm = CreateLoginForm(request.form)
        if request.method == 'POST' and createLoginForm.validate():

            try:
                db = shelve.open('database/user_database/user.db', 'r')
                username = request.form['username']
                password = request.form['password']
                for user in db:
                    user=db[user]
                    if user.get_username()==username and pbkdf2_sha256.verify(password,user.get_user_password())==True:
                        session['logged_in'] = True
                        session['user_id']=user.get_user_id()
                        session['name']=user.get_user_fullname()
                        if request.form['remember']:
                            session['remember']=True

                db.close()
            except:
                print("Error")
            return redirect(url_for('landing_page'))


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


#Delivery Management
@app.route('/SellerDelivery')
def seller_deliverystat():
    #deliverydict={}
    #db=shelve.open('database/delivery_database/delivery.db','r')
    #for key in db:
#
    #db.close()
    return render_template('seller_delivery_status.html')
#add in additional codes to read data from database :(

if __name__ == "__main__":
    app.run(debug=True)



