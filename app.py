from flask import *
import os
from Forms import Create_Product_Form
from werkzeug.datastructures import CombinedMultiDict,FileStorage
from werkzeug import secure_filename
from model import *
app = Flask(__name__)
app.secret_key = "sadbiscuit"
app.config["PRODUCT_IMAGE_UPLOAD"] = "database/product_database/product_images"

@app.route("/")
def landing_page():
    return render_template('home_page.html')
@app.route("/createp",methods=['POST', 'GET'])
           
def product_create():
    Product_Form = Create_Product_Form(CombinedMultiDict((request.files, request.form)))
    filenames = []
    if request.method == 'POST'  :
         #product_pics = request.files.getlist(Product_Form.product_images)
         product_pics = Product_Form.product_images.data
         for i in product_pics:
             filename = secure_filename(i.filename)
             i.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOAD"],secure_filename(i.filename)))
             filenames.append(filename)
         Add_New_Products(Product_Form.product_name.data,Product_Form.product_Quantity.data,Product_Form.product_Description.data,Product_Form.product_Selling_Price.data,
          Product_Form.product_Discount.data,Product_Form.product_catergory.data,filenames)
         
        
    return render_template('productcreateform.html',form =Product_Form )
if __name__ == "__main__":
    app.run(debug=True)


