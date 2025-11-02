from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from models import User

class RegistrationForm(FlaskForm):
    """
    User registration form
    User registration အတွက် form (နာမည်၊ email၊ password)
    """
    name = StringField('Full Name', 
                      validators=[DataRequired(), Length(min=2, max=100)])
    
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=6)])
    
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        """Check if email already exists - Email ရှိပြီးသားလား စစ်မယ်"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


class LoginForm(FlaskForm):
    """
    User login form
    Login ဝင်ဖို့ form (email နဲ့ password)
    """
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    
    submit = SubmitField('Login')


class CarForm(FlaskForm):
    """
    Car management form (Admin)
    Admin က ကား add/edit လုပ်ဖို့ form
    """
    brand = StringField('Brand', 
                       validators=[DataRequired(), Length(max=50)])
    
    model = StringField('Model', 
                       validators=[DataRequired(), Length(max=50)])
    
    year = IntegerField('Year', 
                       validators=[DataRequired(), NumberRange(min=1900, max=2030)])
    
    price_per_day = FloatField('Price Per Day (MMK)', 
                              validators=[DataRequired(), NumberRange(min=0)])
    
    image_url = StringField('Image URL', 
                           validators=[Length(max=200)])
    
    description = TextAreaField('Description')
    
    submit = SubmitField('Save Car')


class BookingForm(FlaskForm):
    """
    Car booking form
    ကား ငှားဖို့ form (စတင်ရက်၊ ပြီးဆုံးရက်)
    """
    start_date = DateField('Start Date', 
                          validators=[DataRequired()], 
                          format='%Y-%m-%d')
    
    end_date = DateField('End Date', 
                        validators=[DataRequired()], 
                        format='%Y-%m-%d')
    
    submit = SubmitField('Book Now')
    
    def validate_end_date(self, end_date):
        """Validate end date is after start date - ပြီးဆုံးရက် က စတင်ရက် ထက် နောက်မှာ ရှိရမယ်"""
        if end_date.data <= self.start_date.data:
            raise ValidationError('End date must be after start date.')


class PaymentForm(FlaskForm):
    """
    Payment form
    Form for selecting payment method
    """
    payment_method = SelectField('Payment Method', 
                                choices=[('credit_card', 'Credit Card'), 
                                        ('cash', 'Cash')],
                                validators=[DataRequired()])
    
    submit = SubmitField('Complete Payment')

