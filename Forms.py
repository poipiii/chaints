from wtforms import Form, StringField, RadioField, SelectField,TextAreaField,IntegerField, validators,SelectMultipleField
from flask_uploads import *
from flask_wtf import FlaskForm
from flask_wtf.file import *
import model

class Create_Product_Form(FlaskForm):
    product_name = StringField('Product Name',validators=[validators.DataRequired()]) 
    product_Description = TextAreaField('Product Description',validators=[validators.DataRequired()]) 
    product_Quantity = IntegerField('Product Selling Price',validators=[validators.DataRequired()])
    product_Selling_Price = IntegerField('Product Selling Price',validators=[validators.DataRequired()])
    product_Discount = IntegerField('Product Name',validators=[validators.DataRequired()]) 
    product_catergory = SelectMultipleField('Gender', [validators.DataRequired()],choices=[('child', 'childern clothing'), ('female', 'Female clothing'), ('male', 'Male Clothing')],default='',render_kw = {'multiple':'multiple','data-live-search':"true"})
    