from flask import *
import os
from Forms import Create_Product_Form
from werkzeug.datastructures import CombinedMultiDict,FileStorage
from flask_dropzone import Dropzone

app = Flask(__name__)
app.secret_key = "sadbiscuit"


@app.route("/")
def landing_page():
    return render_template('home_page.html')
@app.route("/createp",methods=['POST', 'GET'])
def product_create():
    Product_Form = Create_Product_Form(request.form)
    if request.method == 'POST' :
         print(Product_Form.product_name.data,Product_Form.product_Description.data,Product_Form.product_Quantity.data,Product_Form.product_Selling_Price.data,
         Product_Form.product_Discount.data,Product_Form.product_catergory.data)
        #print(form.product_name.data)
    return render_template('productcreateform.html',form =Product_Form )
if __name__ == "__main__":
    app.run(debug=True)


