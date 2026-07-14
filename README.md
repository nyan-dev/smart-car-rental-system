> **Context:** This is a side project demonstrating a full-stack Flask web app. It is not part of the thesis research — the thesis focuses on ML anomaly detection in healthcare/fisheries.

# Smart Car Rental System

## 🚗 About This Project

**Smart Car Rental System** is a web-based platform built with Flask, allowing users to register, browse available cars, book cars, make payments, and view their booking history. Administrators have a separate dashboard to manage cars, approve/reject bookings, and view site-wide reports. This project is suited for learning web development, rapid prototyping, and as a showcase for how a real-world mini SaaS project works.

***

## Table of Contents

- Features
- Business Logic & User Flows
- System Design (Architecture)
- Database Models
- Screenshots (suggested: put images here!)
- Getting Started (Setup & Running)
- Deployment Guide (GitHub & Render)
- License

***

## ✅ Features

### For Customers
- **Registration & Login:** Secure sign-up and login for users.
- **Browse Cars:** See a list of all available cars with photos and details.
- **Book Car:** Choose rental dates and make a booking.
- **Payment:** Choose payment method (Credit/Cash) and complete booking.
- **View Bookings:** See past and current bookings, with statuses (Pending, Confirmed, Rejected).

### For Admins
- **Admin Login:** Special admin users can access the admin dashboard.
- **Manage Cars:** Add, edit, or delete car listings.
- **Booking Approvals:** See all pending bookings; approve or reject each booking with a click.
- **Car Availability:** Confirmed bookings automatically make cars unavailable until the end date.
- **View All Bookings:** See bookings history of all users.
- **Simple Analytics:** (Optional) See site metrics like total bookings, total revenue, available cars, etc.

***

## 🔁 Business Logic & User Flows

### Customer Flow

1. **Register Account** → **Login**
2. **Browse** from the "Homepage" or "Browse Cars" menu
3. Select a Car → Click "Book Now" (if available)
4. Choose start & end dates → Continue to Payment
5. Select payment type → Complete booking
6. Booking goes to "Pending" status (awaiting admin review)
7. Admin either approves (Confirmed) or rejects (booking disappears)
8. User can always see status from "My Bookings"

### Admin Flow

1. **Login** as admin user
2. Access "Admin Dashboard" via menu
3. See all cars & all bookings
4. Approve/reject pending bookings (car becomes unavailable when approved)
5. Add new cars, edit car info, or remove outdated listings

***

## 🗂️ System Components

- **Flask (Python):** Main backend (routes, forms, database)
- **Flask-Login:** Secure user login/session management
- **Flask-WTF:** Secure HTML forms
- **SQLite:** Easy, portable database for rapid dev/testing
- **Bootstrap CSS:** Responsive, modern interface

### Main Files/Folders

- `app.py` — Main application logic, routes, and controls
- `templates/` — All HTML files (with re-usable `base.html`)
- `static/` — Images, CSS, etc.
- `models.py` — Database models (User, Car, Booking, Payment)
- `forms.py` — Flask-WTF forms for user inputs

***

## 🗃️ Database Models

**User**
- id, name, email, password (hashed), role (“customer” or “admin”)

**Car**
- id, brand, model, year, price_per_day, is_available (T/F), image_url, description

**Booking**
- id, user_id, car_id, start_date, end_date, total_price, status (“pending”, “confirmed”, “rejected”), created_at

**Payment**
- id, booking_id, amount, payment_method (“credit_card”, “cash”), payment_status (“paid”), created_at

***

## 🚦 How It Works

- Booking a car sets `Booking.status = "pending"`, car may be reserved or not available.
- Admin reviews "pending" bookings, approves (confirmed) or rejects.
- Only available cars can be booked; when approved, their `is_available = False`.
- All role-based access is enforced at the backend with Flask decorators.
- Payment info is simple and for demonstration only.

***

## 📷 Example Screens (add your screenshots here!)

- Homepage with intro banner and call to action
- Browse cars (cards with images/badges)
- Booking form & Payment step
- User “My Bookings” page with badge statuses
- Admin dashboard with car grids and pending list

***

## 🛠️ Getting Started

**1. Clone the repo:**
```
git clone https://github.com/yourusername/smart-car-rental-system.git
cd smart-car-rental-system
```
**2. Create a virtual environment & activate:**
```
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
**3. Install dependencies:**
```
pip install -r requirements.txt
```
**4. Run app for the first time:**
```
python app.py
```
Access on http://127.0.0.1:5000

> ❗ **Default car data is reset in demo mode. Remove the add_sample_cars() line for production!**

***

## 🌐 Deployment (GitHub + Render.com Quick Guide)

1. Push to GitHub (see details above)
2. Go to [Render.com](https://render.com/), create new "Web Service"
3. Connect with your repo, select Python, set:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
4. Choose Free plan, deploy. Enjoy your live demo!

***

## FAQ

- **Where is the database?**  
  SQLite file in `/instance/` folder. Can swap for MySQL/Postgres for bigger projects.

- **Can I edit the database?**  
  Yes—use DB Browser for SQLite, or the Admin panel for cars/bookings!

- **How to create an admin?**  
  Register a user, then (in DB Browser) set their `role = 'admin'`.

***

## 📢 Credits

- Built by: [Your Name or Team]
- Based on open source technologies.

***

## License

MIT License (see LICENSE file)

***

***

# Smart Car Rental System (မြန်မာ Version)

## ဤ Project အကြောင်း

Smart Car Rental System သည် Flask နဲ့တည်ဆောက်ထားပြီး Web Browser မှတဆင့် ငှားရမ်းသူများသည် အသုံးပြုသူအဖြစ် စာရင်းသွင်းနိုင်၊ ငှားမည့် ကားများကြည့်ရှုနိုင်၊ Booking လုပ်နိုင်၊ ငွေပေးချေမှုလုပ်နိုင်ပါသည်။ အက်ဒ်မင်အသီးသီးသည် Car Management, Booking Approve / Reject လုပ်နိုင်သည်။

***

## (Features)

- အသုံးပြုသူအတွက်
   - စာရင်းသွင်းခြင်း၊ Login
   - ပိုင်ဆိုင်နိုင်သည့် ကားစာရင်း ကြည့်ရှုခြင်း
   - ကားငှားမှု Book Now
   - ငွေပေးချေမှုစနစ် (Credit/Cash)
   - သုံးစွဲသူ Booking မှတ်တမ်းကြည့်ရှုခြင်း
- Admin အတွက်
   - Admin Dashboard (Cars Manage, User Booking Approve/Reject)
   - Car Add/Edit/Delete နိုင်
   - Pending Booking Approve/Reject
   - အာမခံပေးမှု, Site-wide Bookings & Short Report

***

## Business Logic & User Flow

- Customer: Register → Login → Browse Cars → Book Now → Payment → Wait for Admin (Pending) → Get Approved/Rejected → View on My Bookings
- Admin: Login → Visit Admin Dashboard → View/Approve/Reject Pending Bookings → Car Add/Edit/Delete

***

## System Structure (Architecture)

- Backend: Flask, Python
- Frontend: HTML, Bootstrap CSS (in templates/)
- Database: SQLite (Easy, local-instance.db file)
- Authentication: Flask-Login
- Role Checking: @login_required, @admin_required Decorators

***

## Database Models

- **User:** id, name, email, password-hash, role
- **Car:** id, brand, model, year, price_per_day, is_available, image_url, description
- **Booking:** id, user_id, car_id, start_date, end_date, total_price, status, created_at
- **Payment:** id, booking_id, amount, payment_method, payment_status, created_at

***

## Getting Started

```
git clone https://github.com/yourusername/smart-car-rental-system.git
cd smart-car-rental-system
python -m venv venv
venv\Scripts\activate      # (Windows)
pip install -r requirements.txt
python app.py
```

Initial Sample Cars, Admin Demo & User Roles များ admin panel တွင် ပြင်နိုင်သည်။

***

## Deployment & Hosting

- GitHub တွင် push လုပ်ပြီး Render/PythonAnywhere/Replit တို့တွင်ဖိုင်တင်နိုင်သည်။
- SQLite db ကို production အတွက် backup လုပ်ပါ။ Admin Flow/CRUD ပါဝင်သည်။

***

## FAQ

- db ဖိုင် ဆုံးရှုံးရင် အချက်အလက်များ ပျောက်ဆုံးနိုင်သည်။ Regular backup လုပ်မှ data ကြာရှည် သိမ်းဆည်းထားနိုင်သည်။
- admin account ပြုလုပ်ရန် Login ပြီး role ကို db browser (I use SQLite DB Browser) ဖြင့် 'admin' ပြောင်းပါ။
- Production db - နာမည်အသစ်ဖြင့် backup file create လုပ်သင့်သည်။
- Usage, bugs, or modify ကို GitHub issue/report ထည့်သုံးနိုင်သည်။

***

## License: MIT (Open Source Use & Educational Purpose)


***
