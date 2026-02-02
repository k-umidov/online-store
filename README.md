Online Store – Digital Marketplace


Welcome to Online Store – a modern e-commerce platform built with Django and modern frontend technologies. Browse, shop, and manage products with smooth animations and interactive UI.

Key Features

Browse products by categories with dynamic filters

Add products to favorites with interactive animations

Shopping cart with real-time updates

Checkout and payment using Stripe (test keys)

Search products instantly

User registration and profile management

Admin order management with dashboards

Popular products and promotions displayed dynamically

Technologies Used

Python – backend logic

Django + Django REST Framework – backend & API

HTML / CSS / JavaScript – frontend interactivity

PostgreSQL / SQLite – database

Stripe – secure online payment

Git / GitHub – version control

VSCode / PyCharm – IDE

Windows – development environment

Installation & Running

Clone the repository:

git clone https://github.com/k-umidov/online-store.git
cd online-store


Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate  # Windows


Install dependencies:

pip install -r requirements.txt


Create a .env file:

SECRET_KEY=django-insecure-XXXX
STRIPE_PUBLIC_KEY=pk_test_XXXX
STRIPE_SECRET_KEY=sk_test_XXXX


Apply database migrations:

python manage.py migrate


Run the development server:

python manage.py runserver

Project Structure
store/
├─ store_onlayn/          # Main store app
│  ├─ models.py           # Product, cart, order models
│  ├─ views.py            # Backend logic
│  ├─ templates/          # HTML templates
│  └─ static/             # CSS, JS, images
├─ media/                 # Uploaded media
├─ store/                 # settings.py, urls.py
└─ manage.py

UI & Animations

Interactive sliders for featured products

Hover effects for buttons and product cards

Smooth add-to-cart animations

Favorites animations when clicking heart icons

Fully responsive layout for mobile, tablet, and desktop

Dynamic page transitions with JS for smooth navigation

Important Notes

.env and SQLite database should never be committed to GitHub

Use Stripe test keys during development

Static files are served via Django staticfiles

Example Workflow

User navigates categories with smooth page transitions

Adds products to cart with animation

Proceeds to checkout using Stripe

Receives confirmation instantly
