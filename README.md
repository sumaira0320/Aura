# Aura | Premium Multi-Category E-Commerce Platform

> **CodeAlpha Internship — Task 1: E-Commerce Website**  
> A full-featured, modern, and responsive e-commerce web application built using Django, Python, HTML5, CSS3, and JavaScript.

---

## 🌟 Overview

**Aura** is a modern e-commerce web application designed with an emphasis on clean aesthetics, seamless user experience, robust backend inventory management, and intuitive administrative controls. 

It provides an end-to-end shopping experience—from exploring curated multi-category product catalogs, managing persistent shopping carts, and placing orders, to a custom **Store Manager Dashboard** with real-time sales metrics and inventory tracking.

---

## 🚀 Key Features

### 🛍️ Customer Storefront
- **Multi-Category Catalog:** Browse products across multiple departments including *Books, Clothing, Electronics, Home & Kitchen, and Sports*.
- **Live Search & Sorting:** Instant search by product title and description; filter by featured items, newest arrivals, and price.
- **Product Details & Ratings:** Rich product pages featuring stock status, related recommendations, and verified customer star ratings & reviews.
- **Shopping Cart & Checkout:**
  - Dynamic session-based cart with quantity updates and stock limit restrictions.
  - Safe transactional checkout (`transaction.atomic`) preventing stock discrepancies and concurrency issues.
  - Transparent order summary including conditional shipping fee calculations.
- **User Account & Wishlist:**
  - Secure registration, authentication, and session handling.
  - Personal profile dashboard with order history, order status tracking, and wishlist management.

### 📊 Custom Store Manager Dashboard (`/store-admin/`)
- **Key Metrics Overview:** Instant analytics for total revenue, total orders, pending shipments, active customers, and low-stock alerts.
- **Product & Category Management (CRUD):** Add, edit, update, or remove products with image uploads and stock controls.
- **Order Lifecycle Management:** View incoming orders, filter by status (Pending, Processing, Shipped, Delivered, Cancelled), and update status.
- **Review Moderation:** Manage and moderate customer feedback and star ratings.
- **Activity Stream:** Real-time log tracking customer views, cart additions, wishlist updates, and orders.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.10+, Django 5.x
- **Database:** SQLite (development / default)
- **Frontend:** HTML5, Modern Vanilla CSS (CSS Variables, Flexbox, Grid), JavaScript
- **Icons & Typography:** SVG Icons, Google Fonts (Inter)
- **Image Handling:** Pillow

---

## 📦 Installation & Setup

Follow these steps to run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/sumaira0320/Aura.git
cd Aura
```

### 2. Create and Activate Virtual Environment
- **Windows:**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Seed Sample Data (Optional)
To populate the store with categories and demo products:
```bash
python seed.py
```

### 6. Create a Superuser / Admin
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Storefront:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Store Manager Dashboard:** [http://127.0.0.1:8000/store-admin/](http://127.0.0.1:8000/store-admin/)
- **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📂 Project Structure

```text
Aura/
├── ecommerce/               # Project configuration (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                   # Main store application
│   ├── admin.py             # Django admin configuration
│   ├── cart.py              # Session-based shopping cart logic
│   ├── context_processors.py
│   ├── dashboard_forms.py   # Admin dashboard forms
│   ├── dashboard_urls.py    # Admin dashboard URL routes
│   ├── dashboard_views.py   # Admin dashboard views & analytics
│   ├── forms.py             # Storefront forms (cart, checkout, reviews)
│   ├── models.py            # Database schema (Product, Order, Review, etc.)
│   ├── urls.py              # Storefront URL routes
│   └── views.py             # Storefront views
├── static/                  # Static assets (CSS, JS, icons)
│   └── css/style.css
├── templates/               # Storefront & Dashboard HTML templates
│   └── store/
├── media/                   # User and product uploaded media files
├── manage.py
├── requirements.txt
├── seed.py
└── README.md
```

---

## 📄 License & Acknowledgments
Developed as part of the **CodeAlpha Web Development Internship**.
All rights reserved © 2026.
