import shelve
from flask import *
import os
from Forms import Create_Product_Form, CreateLoginForm, CreateUserForm, CreateUpdateForm
from werkzeug.datastructures import CombinedMultiDict,FileStorage
from werkzeug import secure_filename
from model import *
from passlib.hash import pbkdf2_sha256
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sadbiscuit"
app.config["PRODUCT_IMAGE_UPLOAD"] = "static/product_images"


#product display currently not working ui not done yet can do other stuff still will not affect
@app.route("/")
def landing_page():
    Products = fetch_products()
    return render_template('home_page.html' ,product_list = Products )

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
    return render_template('staff_dashboard.html')

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
    Product_Form = Create_Product_Form(CombinedMultiDict((request.files, request.form)))
    filenames = []
    #take in more than 1 images from form, rename images and upload to static/product_images
    if request.method == 'POST'  and Product_Form.validate():
        #product_pics = request.files.getlist(Product_Form.product_images)
        product_pics = Product_Form.product_images.data
        for i in product_pics:
             filename = secure_filename(i.filename)
             i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
             filenames.append(filename)
        #pass form data to Edit_Products function in model.py
        Edit_Products(session.get('user_id'),productid,Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)
        return redirect(url_for('dashboard_products'))      
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
    createUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and createUserForm.validate():
        try:
            db = shelve.open('database/user_database/user.db', 'c')
            user = User_Model(createUserForm.email.data,
createUserForm.username.data, createUserForm.password.data,
createUserForm.firstname.data, createUserForm.lastname.data,createUserForm.role.data)
            db[user.get_user_id()]=user
            db.close()
        except:
            print("Error in retrieving Users from database.")

        return redirect(url_for("landing_page"))
    return render_template('Signup.html', form=createUserForm)

#retrieve User to check db if input correctly
#will move it to admin side after ui finished
@app.route('/retrieveUsers')
def retrieveUsers():
    usersDict = {}
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

                db.close()
            except:
                print("Error")
            return redirect(url_for('landing_page'))


    return render_template('login.html', form=createLoginForm)

#pop the session['logged_in'] out so will redirect to normal main page
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
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


#Delivery Management
@app.route('/SellerDelivery')
def seller_deliverystat():
    return render_template('seller_delivery_status.html')
#add in additional codes to read data from database :(

if __name__ == "__main__":
    app.run(debug=True)



