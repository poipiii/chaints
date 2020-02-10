from wtforms import Form, FileField,StringField, RadioField, SelectField, TextAreaField, IntegerField, validators,SelectMultipleField, MultipleFileField, validators, PasswordField, BooleanField,FloatField
from wtforms.validators import EqualTo, DataRequired, Email
from wtforms.fields.html5 import DateField



class Create_Product_Form(Form):
    product_name = StringField('Product Name',validators=[validators.InputRequired()]) 
    product_Description = TextAreaField('Product Description',validators=[validators.InputRequired()]) 
    product_Quantity = IntegerField('Product Quantity',validators=[validators.InputRequired()])
    product_Selling_Price = FloatField('Product Selling Price',validators=[validators.InputRequired()])
    product_Discount = FloatField('Product Discount',validators=[validators.InputRequired()]) 
    product_catergory = SelectMultipleField('Catergory', validators=[validators.InputRequired()],choices=[('child', 'childern clothing'), ('female', 'Female clothing'), ('male', 'Male Clothing')],default='',render_kw = {'multiple':'multiple','data-live-search':"true"})
    product_images =MultipleFileField('File(s) Upload', validators=[validators.InputRequired()])


class Edit_Product_Form(Form):
    product_name = StringField('Product Name',validators=[validators.InputRequired()]) 
    product_Description = TextAreaField('Product Description',validators=[validators.InputRequired()]) 
    product_Quantity = IntegerField('Product Quantity',validators=[validators.DataRequired()])
    product_Selling_Price = FloatField('Product Selling Price',validators=[validators.InputRequired()])
    product_Discount = FloatField('Product Discount',validators=[validators.InputRequired()]) 
    product_catergory = SelectMultipleField('Catergory', validators=[validators.InputRequired()],choices=[('child', 'childern clothing'), ('female', 'Female clothing'), ('male', 'Male Clothing')],default='',render_kw = {'multiple':'multiple','data-live-search':"true"})
    product_images =MultipleFileField('File(s) Upload')

class update_Quantity_Form(Form):
    product_Quantity = IntegerField('Product Quantity',validators=[validators.InputRequired()])

class CreateUserForm(Form):
 email = StringField('Email', [validators.Length(min=1,
max=150), validators.DataRequired(), validators.email()])
 username = StringField('Username', [validators.Length(min=1,
max=150), validators.DataRequired()])
 password = PasswordField('Password', [validators.Length(min=1,
max=150), validators.DataRequired(),EqualTo('confirm', message='Passwords must match')])
 confirm = PasswordField('Confirm Password', [validators.Length(min=1,
max=150), validators.DataRequired()])
 firstname = StringField('First name', [validators.Length(min=1,
max=150), validators.DataRequired()])
 lastname = StringField('Last name', [validators.Length(min=1,
max=150), validators.DataRequired()])
 role = RadioField('Role', choices=[('B', 'Buyer'),
('S','Seller')], default='B')

class CreateLoginForm(Form):
 username = StringField('Username', [validators.Length(min=1,
max=150), validators.DataRequired()])
 password = PasswordField('Password', [validators.Length(min=1,
max=150), validators.DataRequired()])
 remember= BooleanField('Remember')

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
('S','Seller')], default='B')


class CreateProfileUpdateForm(Form):
    email = StringField('Email', [validators.Length(min=1,
max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1,
max=150), validators.DataRequired()])
    firstname = StringField('First name', [validators.Length(min=1,
max=150), validators.DataRequired()])
    lastname = StringField('Last name', [validators.Length(min=1,
max=150), validators.DataRequired()])
    profile_picture = FileField('Update Profile Picture')

class DeliveryForm(Form):
    address= StringField('Address', [validators.length(min=1,max=150),validators.DataRequired()])
    country= SelectField('Country', [validators.DataRequired()], choices=[('AF', 'Afghanistan'), ('AX', 'Åland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua & Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AC', 'Ascension Island'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia & Herzegovina'), ('BW', 'Botswana'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('IC', 'Canary Islands'), ('CV', 'Cape Verde'), ('BQ', 'Caribbean Netherlands'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('EA', 'Ceuta & Melilla'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo - Brazzaville'), ('CD', 'Congo - Kinshasa'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', 'Côte d’Ivoire'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Curaçao'), ('CY', 'Cyprus'), ('CZ', 'Czechia'), ('DK', 'Denmark'), ('DG', 'Diego Garcia'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HN', 'Honduras'), ('HK', 'Hong Kong SAR China'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('XK', 'Kosovo'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Laos'), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao SAR China'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar (Burma)'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('KP', 'North Korea'), ('MK', 'North Macedonia'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestinian Territories'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn Islands'), ('PL', 'Poland'), ('PT', 'Portugal'), ('XA', 'Pseudo-Accents'), ('XB', 'Pseudo-Bidi'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Réunion'), ('RO', 'Romania'), ('RU', 'Russia'), ('RW', 'Rwanda'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'São Tomé & Príncipe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia & South Sandwich Islands'), ('KR', 'South Korea'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('BL', 'St. Barthélemy'), ('SH', 'St. Helena'), ('KN', 'St. Kitts & Nevis'), ('LC', 'St. Lucia'), ('MF', 'St. Martin'), ('PM', 'St. Pierre & Miquelon'), ('VC', 'St. Vincent & Grenadines'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard & Jan Mayen'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syria'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad & Tobago'), ('TA', 'Tristan da Cunha'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks & Caicos Islands'), ('TV', 'Tuvalu'), ('UM', 'U.S. Outlying Islands'), ('VI', 'U.S. Virgin Islands'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VA', 'Vatican City'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis & Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')] ,render_kw = {'data-live-search':"true"})
    city= StringField('City',[validators.length(min=4),validators.DataRequired()])
    state= StringField('State',[validators.length(min=5),validators.DataRequired()])
    zip= StringField('Zip',[validators.length(min=4),validators.DataRequired()])

class Payment_Form(Form):
    cardholder= StringField('Cardholder name',[validators.length(min=1,max=150),validators.DataRequired()])
    cardno= IntegerField('Card Number',validators=[validators.InputRequired()])
    expiry=StringField('Date Of Expiry',validators=[validators.InputRequired()])
    cvc=StringField('CVC',[validators.length(min=3,max=3),validators.DataRequired()])

class GetEmailForm(Form):
 email = StringField('Email', [validators.Length(min=1,
max=150), validators.DataRequired()])

class PasswordReset(Form):
 password = PasswordField('Password', [validators.Length(min=1,
max=150), validators.DataRequired(),EqualTo('confirm', message='Passwords must match')])
 confirm = PasswordField('Confirm Password', [validators.Length(min=1,
max=150), validators.DataRequired()])


class updateorderForm(Form):
   orderqty = IntegerField('Quantity',validators=[validators.InputRequired()])


class NewStatus(Form):
    deliverystatus=SelectField('Status',[validators.Optional()],choices=[('Pending','Pending'),('Order Processing','Order Processing'),('Order Dispatched','Order Dispatched'),('Order Returned','Order Returned')],default='')

class CarrierForm(Form):
    orderid=StringField('Order ID',[validators.Length(min=1,max=150),validators.DataRequired()])
    updatedate=DateField('Date of Status', [validators.DataRequired(message=())], format='%Y-%m-%d')
    country=SelectField('Country',[validators.DataRequired()],choices=[('AF', 'Afghanistan'), ('AX', 'Åland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola')])
    status=SelectField('Status',[validators.DataRequired()],choices=[('Info Received','Info Received'),('In Transit','In Transit'),('Out for Delivery','Out for Delivery'),('Failed Attempt','Failed Attempt'),('Delivered','Delivered'),('Delayed','Delayed')])
    deliverynotes=TextAreaField('Notes',[validators.DataRequired(),validators.Length(min=1,max=100)])

class CarrierUpdateForm(Form):
    status=SelectField('Status',[validators.DataRequired()],choices=[('Info Received','Info Received'),('In Transit','In Transit'),('Out for Delivery','Out for Delivery'),('Failed Attempt','Failed Attempt'),('Delivered','Delivered'),('Delayed','Delayed')])
    deliverynotes=TextAreaField('Notes',[validators.DataRequired(),validators.Length(min=1,max=100)])
    country=SelectField('Country',[validators.DataRequired()],choices=[('AF', 'Afghanistan'), ('AX', 'Åland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola')])

class CarrierBuyer(Form):
    orderid=StringField('Tracking ID',[validators.Length(min=1,max=150),validators.DataRequired()])

class Question(Form):
    mtitle= TextAreaField("",[validators.DataRequired(),validators.Length(min=1,max=60)])
    mbody=TextAreaField("",[validators.Optional(),validators.Length(min=1,max=100)])

class Response(Form):
    Response=TextAreaField("Response",[validators.DataRequired(),validators.Length(min=1,max=100)])

class FAQd(Form):
    question= TextAreaField("",[validators.DataRequired(),validators.Length(min=1,max=60)])
    answer=TextAreaField("",[validators.Optional(),validators.Length(min=1,max=100)])


class review_form(Form):
    rating= SelectField('Rating', [validators.DataRequired()], choices=[('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)])
    review_text = TextAreaField("write your review here",[validators.DataRequired()])
