from wtforms import Form, StringField, RadioField, SelectField,TextAreaField,IntegerField, validators,SelectMultipleField,MultipleFileField
from flask_uploads import *
from flask_wtf import FlaskForm ,file
from flask_wtf.file import *
import model

class Create_Product_Form(FlaskForm):
    product_name = StringField('Product Name',validators=[validators.InputRequired()]) 
    product_Description = TextAreaField('Product Description',validators=[validators.InputRequired()]) 
    product_Quantity = IntegerField('Product Quantity',validators=[validators.InputRequired()])
    product_Selling_Price = IntegerField('Product Selling Price',validators=[validators.InputRequired()])
    product_Discount = IntegerField('Product Discount',validators=[validators.InputRequired()]) 
    product_catergory = SelectMultipleField('Catergory', validators=[validators.InputRequired()],choices=[('child', 'childern clothing'), ('female', 'Female clothing'), ('male', 'Male Clothing')],default='',render_kw = {'multiple':'multiple','data-live-search':"true"})
    product_images =MultipleFileField('File(s) Upload', validators=[validators.InputRequired()])
