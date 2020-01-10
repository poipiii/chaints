import shelve
from flask import *
import os
from Forms import Create_Product_Form, CreateLoginForm, CreateUserForm
from werkzeug.datastructures import CombinedMultiDict,FileStorage
from werkzeug import secure_filename
from model import *
from passlib.hash import pbkdf2_sha256
from Forms import Question, Response
app = Flask(__name__)
app.secret_key = "sadbiscuit"
app.config["PRODUCT_IMAGE_UPLOAD"] = "static/product_images"


#product display currently not working ui not done yet can do other stuff still will not affect
@app.route("/")
def landing_page():
    if session.get('logged_in') == True:
        return redirect(url_for('home_loginpage'))
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

@app.route("/home_login_page")
def home_loginpage(): 
    return render_template('home_login_page.html')




@app.route("/dashboard")
def dashboard_home():
    return render_template('staff_dashboard.html')

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
    if request.method == 'POST'  and Product_Form.validate_on_submit():
        #product_pics = request.files.getlist(Product_Form.product_images)
        product_pics = Product_Form.product_images.data
        for i in product_pics:
             filename = secure_filename(i.filename)
             i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
             filenames.append(filename)
        #pass form data to Edit_Products function in model.py
        Edit_Products(session.get('user_id'),productid,Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)

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
        except:
            print("Error in retrieving Users from database.")
        db.close()
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
#FAQ Display
@app.route('/FAQ')
def FAQ():
    Gold=[]
    try:
        Ein=shelve.open("database/forum_database/FAQQ.db","r")
        Enamel=Ein.values()
        for i in Enamel:
            if isinstance(i,CQuestion):
                Gold.append(i)

        Ein.close()

    except IOError:
        print("Database not found")
    return render_template('FAQ.html', Gold=Gold)

#Forum Question
@app.route('/createQns',methods=["GET","POST"])
def createQns():
    createquestion=Question(request.form)
    if request.method=="POST" and createquestion.validate():

        new_question = CQuestion('123456',createquestion.mtitle.data,createquestion.mbody.data)
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
        Respondents= CAnswer("6","",Reply.Response.data)
        try:
            dennis=shelve.open('database/forum_database/FAQQ.db','c')
            dennis[Respondents.get_ansid()]=Respondents
            
        except:
            print("Something screwed up")

        dennis.close()
        RespondtoQns(Respondents.get_ansid(),id)
        return redirect(url_for('displayQns'))
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
if __name__ == "__main__":
    app.run(debug=True)



