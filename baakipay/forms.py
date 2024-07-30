from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Email
from flask_wtf.file import FileField, FileRequired
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
# Import Customer model
from .models import Customer


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = Customer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')
    
    def validate_username(self, username):
        user = Customer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already in use. Please choose a different one.')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), 
        Length(min=6), 
        EqualTo('new_password', message='Passwords must match')
    ])
    change_password = SubmitField('Change Password')

    def validate_new_password(self, field):
        if field.data == self.current_password.data:
            raise ValidationError('New password must be different from the current password.')
        
class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Product Picture', validators=[DataRequired()])
    flash_sale = BooleanField('Flash Sale')

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update')


class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[
        ('Pending', 'Pending'), 
        ('Accepted', 'Accepted'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'), 
        ('Canceled', 'Canceled')
    ])
    update = SubmitField('Update Status')

class ComplaintForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Your Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    message = TextAreaField('Complaint Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Complaint')
