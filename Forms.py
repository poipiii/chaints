from wtforms import Form, StringField, RadioField, SelectField,TextAreaField,IntegerField, validators,SelectMultipleField,MultipleFileField,validators

class Create_Product_Form(Form):
    product_name = StringField('Product Name',validators=[validators.InputRequired()]) 
    product_Description = TextAreaField('Product Description',validators=[validators.InputRequired()]) 
    product_Quantity = IntegerField('Product Quantity',validators=[validators.InputRequired()])
    product_Selling_Price = IntegerField('Product Selling Price',validators=[validators.InputRequired()])
    product_Discount = IntegerField('Product Discount',validators=[validators.InputRequired()]) 
    product_catergory = SelectMultipleField('Catergory', validators=[validators.InputRequired()],choices=[('child', 'childern clothing'), ('female', 'Female clothing'), ('male', 'Male Clothing')],default='',render_kw = {'multiple':'multiple','data-live-search':"true"})
    product_images =MultipleFileField('File(s) Upload', validators=[validators.InputRequired()])

class CreateUserForm(Form):
 email = StringField('Email', [validators.Length(min=1,
max=150), validators.DataRequired()])
 username = StringField('Username', [validators.Length(min=1,
max=150), validators.DataRequired()])
 password = StringField('Password', [validators.Length(min=1,
max=150), validators.DataRequired()])
 firstname = StringField('First name', [validators.Length(min=1,
max=150), validators.DataRequired()])
 lastname = StringField('Last name', [validators.Length(min=1,
max=150), validators.DataRequired()])
 role = RadioField('Role', choices=[('B', 'Buyer'),
('A','Admin')], default='B')

class CreateLoginForm(Form):
 username = StringField('Username', [validators.Length(min=1,
max=150), validators.DataRequired()])
 password = StringField('Password', [validators.Length(min=1,
max=150), validators.DataRequired()])

class CreateUpdateForm(Form):
 email = StringField('Email', [validators.Length(min=1,
max=150), validators.DataRequired()])
 username = StringField('Username', [validators.Length(min=1,
max=150), validators.DataRequired()])
 firstname = StringField('First name', [validators.Length(min=1,
max=150), validators.DataRequired()])
 lastname = StringField('Last name', [validators.Length(min=1,
max=150), validators.DataRequired()])
 role = RadioField('Role', choices=[('B', 'Buyer'),
('A','Admin')], default='B')
