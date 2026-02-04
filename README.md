🛍️ Online Store – Modern E-commerce Platform
🚀 Overview
Online Store is a dynamic, animation-rich e-commerce platform built with Django and modern frontend technologies. It offers a seamless shopping experience with interactive animations, smooth transitions, and intuitive user interface.

✨ Key Features
Interactive Product Browsing with animated category filters

Smart Shopping Cart with real-time visual updates

Stripe-Powered Checkout with animated payment flows

Favorites System with heart explosion animations

Live Search with typewriter-style suggestions

Admin Dashboard with animated statistics

Fully Responsive with device-optimized animations

🛠️ Quick Installation Guide
1. Clone & Setup
bash
# Clone the repository
git clone https://github.com/k-umidov/online-store.git
cd online-store

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
2. Install Dependencies
bash
pip install -r requirements.txt
3. Configure Environment
Create .env file in project root:

bash
SECRET_KEY=your-secret-key-here
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
4. Database Setup
bash
# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter: username, email, password
5. Launch Development Server
bash
python manage.py runserver
🔐 Accessing Admin Panel
1. Start the Server
bash
python manage.py runserver
# Server runs at: http://localhost:8000
2. Open Admin Panel
URL: http://localhost:8000/admin/

Username: admin (or your created username)

Password: Your chosen password during createsuperuser

3. Admin Features
User Management – Customers & staff

Product Catalog – Add/edit products with images

Order Processing – View & manage orders

Category Management – Product organization

Review Moderation – Customer feedback

Coupon System – Discount management

📱 Quick Commands
bash
# Run server
python manage.py runserver

# Create admin
python manage.py createsuperuser

# Reset password
python manage.py changepassword admin

# Load sample data
python manage.py loaddata fixtures/products.json
🚨 Troubleshooting
Common Issues:
bash
# Port already in use
python manage.py runserver 8080

# Migration errors
python manage.py makemigrations
python manage.py migrate

# Static files not loading
python manage.py collectstatic
Admin Login Issues:
Ensure superuser was created: python manage.py createsuperuser

Check server is running: http://localhost:8000

Verify credentials are correct

Try password reset: python manage.py changepassword username

📦 Project Structure
text
online-store/
├── store/                 # Main Django project
├── store_onlayn/         # Store app (products, cart, orders)
├── media/               # Uploaded images
├── static/              # CSS, JS, animations
└── templates/           # HTML with animated components
🌟 Ready to Go!
Store Frontend: http://localhost:8000
Admin Panel: http://localhost:8000/admin/

Enjoy your modern e-commerce platform with stunning animations! 🎉

Note: Use Stripe test keys for development. Never commit .env file to version control.
