from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from models import User

class CustomerRegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=7, max=15)])
    
    # 🇮🇳 Indianized Pincode field added with strict 6-digit number criteria
    pincode = StringField('6-Digit Area Pincode Indicator', validators=[
        DataRequired(), 
        Length(min=6, max=6, message="Pincode must be exactly 6 digits."),
        Regexp(r'^[0-9]+$', message="Pincode must contain only numbers.")
    ])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = TextAreaField('Home Address', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    sku = StringField('Item Code / SKU', validators=[DataRequired()])
    barcode = StringField('Barcode (Optional)')
    brand = StringField('Brand / Company')
    description = TextAreaField('Product Description')
    cost_price = FloatField('Buying Price (₹)', validators=[DataRequired()])
    selling_price = FloatField('Selling Price (₹)', validators=[DataRequired()])
    stock_quantity = IntegerField('Initial Stock Stock Level', validators=[DataRequired()])
    min_stock_level = IntegerField('Minimum Low Stock Alert Level', validators=[DataRequired()])
    category_id = SelectField('Category Link', coerce=int, validators=[DataRequired()])
    product_image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Save Product')

class CheckoutForm(FlaskForm):
    pickup_date = StringField('Pickup Date (YYYY-MM-DD)', validators=[DataRequired()])
    pickup_time_slot = SelectField('Preferred Pickup Time Window Slot', choices=[
        ('08:00 AM - 10:00 AM', '08:00 AM - 10:00 AM'),
        ('10:00 AM - 12:00 PM', '10:00 AM - 12:00 PM'),
        ('12:00 PM - 02:00 PM', '12:00 PM - 02:00 PM'),
        ('02:00 PM - 04:00 PM', '02:00 PM - 04:00 PM'),
        ('04:00 PM - 06:00 PM', '04:00 PM - 06:00 PM'),
        ('06:00 PM - 08:00 PM', '06:00 PM - 08:00 PM')
    ], validators=[DataRequired()])
    notes = TextAreaField('Special Notes / Instructions')
    submit = SubmitField('Confirm Pickup Booking')