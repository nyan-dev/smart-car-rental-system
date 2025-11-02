from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Database instance
# Database object ကို ဆောက်မယ် (app.py မှာ initialize လုပ်မယ်)
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User model for customers and administrators
    User table - customer တွေနဲ့ admin တွေ သိမ်းဖို့
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')  # 'customer' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One user can have many bookings
    # User တစ်ယောက်က booking အများကြီး လုပ်လို့ရတယ်
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password - Password ကို encrypt လုပ်ပြီး သိမ်းမယ်"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password - Password မှန်/မမှန် စစ်မယ်"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin - Admin လား မဟုတ်လား စစ်မယ်"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.email}>'


class Car(db.Model):
    """
    Car model for rental cars
    Car table - လာငှားလို့ရတဲ့ ကားတွေ သိမ်းဖို့
    """
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), default='default-car.jpg')
    is_available = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One car can have many bookings
    # ကား တစ်စီးကို အကြိမ်ပေါင်းများစွာ ငှားလို့ရတယ်
    bookings = db.relationship('Booking', backref='car', lazy=True)
    
    def __repr__(self):
        return f'<Car {self.brand} {self.model}>'


class Booking(db.Model):
    """
    Booking model for car rentals
    Booking table - ကားငှားတဲ့ records တွေ သိမ်းဖို့
    """
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One booking has one payment
    # Booking တစ်ခုမှာ payment တစ်ခု ရှိမယ်
    payment = db.relationship('Payment', backref='booking', uselist=False, lazy=True)
    
    def calculate_days(self):
        """Calculate rental duration - ငှားမဲ့ ရက်အရေအတွက် တွက်မယ်"""
        return (self.end_date - self.start_date).days
    
    def __repr__(self):
        return f'<Booking {self.id} - User {self.user_id}>'


class Payment(db.Model):
    """
    Payment model for booking payments
    Payment table - ငွေပေးချေမှု records တွေ သိမ်းဖို့
    """
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='credit_card')  # 'credit_card', 'cash'
    payment_status = db.Column(db.String(20), default='pending')  # 'pending', 'paid', 'failed'
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.id} - Booking {self.booking_id}>'
