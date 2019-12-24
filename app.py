import shelve
from flask import *
import os
from Forms import Create_Product_Form, CreateLoginForm, CreateUserForm
from werkzeug.datastructures import CombinedMultiDict,FileStorage
from werkzeug import secure_filename
from model import *


app = Flask(__name__)
app.secret_key = "sadbiscuit"
app.config["PRODUCT_IMAGE_UPLOAD"] = "static/product_images"


#product display currently not working ui not done yet can do other stuff still will not affect
@app.route("/")
def landing_page():
    #Products = fetch_products()
    #return render_template('home_page.html' ,product_list = Products )
    return render_template('home_page.html')

#currently not working ui not done yet whatsapp me before touching this  
# @app.route("/product/<productid>")
# def product_page(productid):
#     get_product = get_product_by_id(productid)
#     return render_template('product_view.html',product = get_product)


@app.route("/dashboard")
def dashboard_home():
    return render_template('staff_dashboard.html')

@app.route("/manage_products",methods=['POST', 'GET'])
def dashboard_products():
    Products = fetch_products()
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
        Add_New_Products(Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)  
        return redirect(url_for('dashboard_products'))      
    return render_template('productcreateform.html',form =Product_Form )
    
#route to update product form
@app.route("/update_products/<productid>",methods=['POST', 'GET'])
def dashboard_edit_products(productid):
    Product_Form = Create_Product_Form(CombinedMultiDict((request.files, request.form)))
    filenames = []
    #take in more than 1 images from form, rename images and upload to static/product_images
    if request.method == 'POST'  and Product_Form.validate_on_submit():
        #product_pics = request.files.getlist(Product_Form.product_images)
        product_pics = Product_Form.product_images.data
        for i in product_pics:
             filename = secure_filename(i.filename)
             i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
             filenames.append(filename)
        #pass form data to Edit_Products function in model.py
        Edit_Products(productid,Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)

    return render_template('productcreateform.html',form =Product_Form)


@app.route("/delete_products/<productid>",methods=['POST'])
def delete_products(productid):
    get_product = get_product_by_id(productid)
    delete_product_by_id(get_product.get_product_id())
    return redirect(url_for('dashboard_products'))





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
        except:
            print("Error in retrieving Users from database.")
        db.close()
        return redirect(url_for("landing_page"))
    return render_template('Signup.html', form=createUserForm)

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

@app.route('/login', methods=('GET', 'POST'))
def loginUser():
    createLoginForm = CreateLoginForm(request.form)
    if request.method == 'POST' and createLoginForm.validate():
        try:
            db = shelve.open('database/user_database/user.db', 'r')
            username = request.form['username']
            password = request.form['password']
            for user in db:
                user=db[user]
                if user.get_username()==username and user.get_user_password()==password:
                    session['id'] = user.get_user_id()
                    session['user_name'] = user.get_username()
                    session['logged_in'] = True
            db.close()
        except:
            print("Error")
        return redirect(url_for('landing_page'))

    return render_template('login.html', form=createLoginForm)


if __name__ == "__main__":
    app.run(debug=True)



