# ⚡ QuickMart — 10-Minute Grocery Delivery App

A full-stack grocery delivery web application built with **Django + Bootstrap 5**, inspired by Blinkit & Zepto.

---

## 🛠️ Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python 3.10+, Django 4.2            |
| Frontend  | HTML5, CSS3, Bootstrap 5.3, JS ES6  |
| Database  | SQLite (dev) / PostgreSQL (prod)    |
| Icons     | Bootstrap Icons                     |
| Fonts     | Google Fonts (Nunito, Poppins)      |

---

## ✨ Features

### 🛍️ Shopping
- 🏠 Beautiful home page with hero banner & categories
- 🔍 Live search with auto-complete dropdown
- 🗂️ Category-wise product browsing
- 📦 Product detail page with zoom & quantity picker
- ❤️ Wishlist management
- 🛒 AJAX-powered cart (no page reload!)
- 🔢 Real-time cart counter in navbar

### 📦 Orders
- ✅ Checkout with address & payment selection
- 📋 Order placement & confirmation
- 🛵 Live order tracking with status steps
- 📜 Order history

### 👤 Auth
- Register / Login / Logout
- User profile with address management
- Demo credentials pre-filled

### 🔧 Admin
- Full Django admin panel
- Category & Product management
- Order status updates
- Customer management

---

## 🚀 Quick Start

### Option 1 – Auto Script (Recommended)
```bash
# 1. Navigate to project folder
cd quickmart

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Run setup script
bash setup_and_run.sh
```

### Option 2 – Manual Steps
```bash
cd quickmart
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py seed_data

python manage.py runserver
```

Then open **http://127.0.0.1:8000** in your browser.

---

## 🔑 Credentials

| Role      | Username  | Password  |
|-----------|-----------|-----------|
| Admin     | admin     | admin123  |
| Test User | testuser  | test123   |

**Admin Panel:** http://127.0.0.1:8000/admin

---

## 📁 Project Structure

```
quickmart/
├── manage.py
├── requirements.txt
├── setup_and_run.sh
├── quickmart/              # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                  # Main app
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── urls.py             # URL routing
│   ├── forms.py            # Django forms
│   ├── admin.py            # Admin config
│   ├── context_processors.py
│   └── management/commands/
│       └── seed_data.py    # Sample data loader
├── templates/store/        # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── product_list.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_success.html
│   ├── orders.html
│   ├── order_detail.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── wishlist.html
│   └── includes/
│       └── product_card.html
└── static/
    ├── css/style.css       # Custom CSS
    └── js/main.js          # Custom JavaScript
```

---

## 🎯 Key Pages

| URL                   | Page              |
|-----------------------|-------------------|
| `/`                   | Home              |
| `/products/`          | Product Listing   |
| `/products/<slug>/`   | Product Detail    |
| `/cart/`              | Shopping Cart     |
| `/checkout/`          | Checkout          |
| `/orders/`            | My Orders         |
| `/profile/`           | User Profile      |
| `/wishlist/`          | Wishlist          |
| `/admin/`             | Admin Panel       |

---

## 🌟 Interview Highlights

- **AJAX Cart** — Add/remove/update without page reload
- **Live Search API** — Real-time product search
- **Context Processors** — Global cart count in all pages
- **Django ORM** — Complex queries with `Q` objects
- **Session + Auth Cart** — Works for both guests & logged-in users
- **Seed Management Command** — `python manage.py seed_data`
- **Responsive Design** — Mobile-first Bootstrap 5

---

Built with ❤️ for learning & interviews.
