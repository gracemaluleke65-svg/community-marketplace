from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, IntegerField, SelectField, RadioField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError, Optional
import re

def validate_phone(form, field):
    phone = field.data
    if not re.match(r'^[0-9]{10}$', phone):
        raise ValidationError('Phone number must be exactly 10 digits')

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), validate_phone])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = TextAreaField('Address', validators=[DataRequired()])
    role = RadioField('I want to', choices=[
        ('buyer', 'Buy Products Only'), 
        ('seller', 'Sell Products Only'),
        ('both', 'Both - Buy AND Sell')
    ], default='buyer')
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price (Rands)', validators=[DataRequired(), NumberRange(min=0.01)])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=1)])
    category = SelectField('Category', choices=[
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('books', 'Books'),
        ('sports', 'Sports'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Product')

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), validate_phone])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], coerce=int)
    comment = TextAreaField('Comment', validators=[Length(max=500)])
    submit = SubmitField('Submit Review')

class UpgradeToSellerForm(FlaskForm):
    submit = SubmitField('Become a Seller')

class CouponForm(FlaskForm):
    code = StringField('Coupon Code', validators=[DataRequired(), Length(min=3, max=50)])
    name = StringField('Coupon Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    discount_type = SelectField('Discount Type', choices=[
        ('percentage', 'Percentage (%)'),
        ('fixed', 'Fixed Amount (R)')
    ], validators=[DataRequired()])
    discount_value = FloatField('Discount Value', validators=[DataRequired(), NumberRange(min=0.01)])
    min_order_amount = FloatField('Minimum Order Amount', validators=[Optional(), NumberRange(min=0)], default=0)
    max_discount_amount = FloatField('Maximum Discount (for percentage coupons)', validators=[Optional(), NumberRange(min=0)])
    applicable_category = SelectField('Applicable Category', choices=[
        ('', 'All Categories'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('books', 'Books'),
        ('sports', 'Sports'),
        ('other', 'Other')
    ], validators=[Optional()])
    applicable_seller_id = IntegerField('Applicable Seller ID (leave blank for all sellers)', validators=[Optional()])
    valid_from = DateTimeField('Valid From', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    valid_to = DateTimeField('Valid To', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    usage_limit = IntegerField('Total Usage Limit (leave blank for unlimited)', validators=[Optional(), NumberRange(min=1)])
    per_user_limit = IntegerField('Uses Per User', validators=[Optional(), NumberRange(min=1)], default=1)
    is_first_purchase_only = BooleanField('First Purchase Only')
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Create Coupon')

class ApplyCouponForm(FlaskForm):
    coupon_code = StringField('Coupon Code', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Apply Coupon')