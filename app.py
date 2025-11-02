# Flask, extensions, forms, and helpers import (အဓိက library တွေ import)
from flask import Flask, render_template, redirect, url_for, flash, session, request, abort
from config import Config
from models import db, User, Car, Booking, Payment
from forms import RegistrationForm, LoginForm, BookingForm, PaymentForm, CarForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import datetime

# ------------------- Admin လိုအပ်တဲ့ Decorator ----------------------
# Admin function တွေသို့ ဝင်ခွင့်ရှိ/မရှိ စစ်သိမ်းရေးယူရန်
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # User login ပြီး admin စစ် (role=='admin') မဟုတ်လျှင် 403 error ပေးမယ်
        if not current_user.is_authenticated or not hasattr(current_user, 'role') or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ------------------- Flask App Initialize --------------------------
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ------------------- Login Manager Initialize ----------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # login မလုပ်ရင် redirect

# User Loader (login user session ကို db record ပြန်သွင်း)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----------------- Admin Dashboard & CRUD Routes --------------------
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    cars = Car.query.all()
    pending_bookings = Booking.query.filter_by(status='pending').all()  # လိုင်စင်မရှိသေးပဲ စောင့်နေသော booking
    bookings = Booking.query.all()
    return render_template('admin_dashboard.html', cars=cars, bookings=bookings, pending_bookings=pending_bookings)

@app.route('/admin/approve_booking/<int:booking_id>')
@login_required
@admin_required
def approve_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'confirmed'
    booking.car.is_available = False
    db.session.commit()
    flash('Booking approved.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject_booking/<int:booking_id>')
@login_required
@admin_required
def reject_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    car = booking.car
    db.session.delete(booking)
    # car.is_available ပြန်ပြောင်းဖို့ဖို့လည်း အခြေအနေအရသာလုပ်မယ်
    db.session.commit()
    flash('Booking rejected and removed.', 'warning')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_car', methods=['GET', 'POST'])
@login_required
@admin_required
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(
            brand=form.brand.data,
            model=form.model.data,
            year=form.year.data,
            price_per_day=form.price_per_day.data,
            image_url=form.image_url.data or 'default-car.jpg',
            description=form.description.data,
            is_available=True
        )
        db.session.add(car)
        db.session.commit()
        flash('Car added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('car_form.html', form=form, action="Add New Car")

@app.route('/admin/edit_car/<int:car_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = CarForm(obj=car)
    if form.validate_on_submit():
        car.brand = form.brand.data
        car.model = form.model.data
        car.year = form.year.data
        car.price_per_day = form.price_per_day.data
        car.image_url = form.image_url.data or 'default-car.jpg'
        car.description = form.description.data
        db.session.commit()
        flash('Car updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('car_form.html', form=form, action="Edit Car")

@app.route('/admin/delete_car/<int:car_id>')
@login_required
@admin_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Car deleted.', 'info')
    return redirect(url_for('admin_dashboard'))

# ----------------- Main User & Customer Routes ---------------------

@app.route('/')
def home():
    # Landing/Homepage ပြရန်
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # သုံးစွဲသူ အသစ်အတွက် Registration Form
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login ဝင်ရန် Form
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    # Logout user
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/cars')
def cars():
    # Car LIST page
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)

# ------------------- Sample Car Data Function (ဖျက်ရန် function) -----------
def add_sample_cars():
    # Demo/test အတွက် သုံးဖို့ cars ကို reset ပြီး အသစ်ထည့်တဲ့ function (prod မှာ ဖျက်ပါ)
    Car.query.delete()
    db.session.commit()
    cars = [
        Car(brand="Toyota", model="Vios", year=2020, price_per_day=50, image_url="default-car.jpg", description="Economical sedan, comfortable and reliable."),
        Car(brand="Honda", model="Civic", year=2021, price_per_day=70, image_url="default-car.jpg", description="Sporty sedan with advanced features."),
        Car(brand="Perodua", model="Myvi", year=2019, price_per_day=35, image_url="default-car.jpg", description="Popular compact car, easy to drive in city."),
        Car(brand="Proton", model="Saga", year=2022, price_per_day=40, image_url="default-car.jpg", description="Budget-friendly local sedan."),
        Car(brand="Nissan", model="Almera", year=2023, price_per_day=45, image_url="default-car.jpg", description="Latest compact sedan."),
        Car(brand="Mazda", model="CX-5", year=2021, price_per_day=80, image_url="default-car.jpg", description="Comfortable SUV with style."),
        Car(brand="BMW", model="320i", year=2018, price_per_day=120, image_url="default-car.jpg", description="Premium sports sedan."),
        Car(brand="Toyota", model="Fortuner", year=2020, price_per_day=130, image_url="default-car.jpg", description="Spacious SUV for big family trips."),
        Car(brand="Honda", model="BR-V", year=2022, price_per_day=85, image_url="default-car.jpg", description="7 seater family-friendly MPV."),
        Car(brand="Ford", model="Ranger", year=2019, price_per_day=100, image_url="default-car.jpg", description="Powerful pick-up truck."),
        Car(brand="Mitsubishi", model="Xpander", year=2023, price_per_day=90, image_url="default-car.jpg", description="Crossover MPV/SUV."),
        Car(brand="Hyundai", model="Starex", year=2017, price_per_day=95, image_url="default-car.jpg", description="Big van for group travel."),
        Car(brand="Kia", model="Picanto", year=2021, price_per_day=30, image_url="default-car.jpg", description="Mini hatchback, urban driving."),
        Car(brand="Toyota", model="Hilux", year=2022, price_per_day=110, image_url="default-car.jpg", description="Heavy duty, good for trips."),
        Car(brand="Mercedes", model="C200", year=2018, price_per_day=140, image_url="default-car.jpg", description="Luxury sedan for VIP ride."),
    ]
    db.session.add_all(cars)
    db.session.commit()

@app.route('/book_car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def book_car(car_id):
    # Car booking for logged-in user
    car = Car.query.get_or_404(car_id)
    form = BookingForm()
    payment_form = PaymentForm()
    if form.validate_on_submit():
        days = (form.end_date.data - form.start_date.data).days
        if days <= 0:
            flash('End date must be after start date.', 'danger')
            return render_template('book_car.html', car=car, form=form, payment_form=payment_form)
        total_price = car.price_per_day * days
        # Session မှာ booking info သိမ်းပြီး payment ပြန်ပြမယ်
        session['booking'] = {
            'car_id': car.id,
            'start_date': str(form.start_date.data),
            'end_date': str(form.end_date.data),
            'total_price': total_price
        }
        return render_template('payment.html', car=car, form=form, payment_form=payment_form, total_price=total_price)
    return render_template('book_car.html', car=car, form=form, payment_form=payment_form)

@app.route('/payment/<int:car_id>', methods=['POST'])
@login_required
def payment(car_id):
    # Payment confirm page
    payment_form = PaymentForm()
    booking_data = session.get('booking')
    if not booking_data or int(booking_data['car_id']) != car_id:
        flash("Invalid booking session. Start over.", "danger")
        return redirect(url_for('cars'))
    car = Car.query.get_or_404(car_id)
    if payment_form.validate_on_submit():
        booking = Booking(
            user_id=current_user.id,
            car_id=car.id,
            start_date=datetime.strptime(booking_data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(booking_data['end_date'], '%Y-%m-%d').date(),
            total_price=booking_data['total_price'],
            status='pending' # Admin approve လုပ်ဖို့လို
        )

        car.is_available = False
        db.session.add(booking)
        db.session.commit()
        pay = Payment(
            booking_id=booking.id,
            amount=booking.total_price,
            payment_method=payment_form.payment_method.data,
            payment_status='paid'
        )
        db.session.add(pay)
        db.session.commit()
        flash(f'Booking and payment successful! RM {booking.total_price}', 'success')
        session.pop('booking', None)
        return redirect(url_for('my_bookings'))
    total_price = booking_data['total_price']
    return render_template('payment.html', car=car, payment_form=payment_form, total_price=total_price)

@app.route('/my_bookings')
@login_required
def my_bookings():
    # User's own bookings/history
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

# ------------------- Start Flask app -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_cars() # <-- production မှာ comment လုပ်/ဖျက်ပါ
    app.run(debug=True)
