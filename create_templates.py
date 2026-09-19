import os

BASE_DIR = r"D:\CodeAlpha\Task1_Ecommerce\templates"

templates = {
    "store/base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}CodeAlpha E-commerce{% endblock %}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2563eb;
            --primary-hover: #1d4ed8;
            --background: #f8fafc;
            --surface: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--background);
            color: var(--text-main);
            line-height: 1.6;
        }
        a { text-decoration: none; color: inherit; }
        header {
            background-color: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .logo { font-size: 1.5rem; font-weight: 700; color: var(--primary-color); }
        .nav-links { display: flex; gap: 1.5rem; align-items: center; }
        .nav-links a { font-weight: 600; transition: color 0.2s; }
        .nav-links a:hover { color: var(--primary-hover); }
        .btn {
            background-color: var(--primary-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: background 0.2s;
        }
        .btn:hover { background-color: var(--primary-hover); color: white;}
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
        .messages { padding: 1rem; margin-bottom: 1rem; border-radius: 0.5rem; }
        .messages.success { background-color: #dcfce7; color: #166534; }
        .messages.error { background-color: #fee2e2; color: #991b1b; }
        
        /* Grid Layouts */
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 2rem;
        }
        .product-card {
            background: var(--surface);
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            transition: transform 0.2s;
        }
        .product-card:hover { transform: translateY(-4px); }
        .product-img { width: 100%; height: 250px; object-fit: cover; background: #e2e8f0; }
        .product-info { padding: 1.5rem; }
        .product-price { font-size: 1.25rem; font-weight: 700; color: var(--primary-color); margin-top: 0.5rem; }
        
        /* Layouts */
        .flex-row { display: flex; gap: 2rem; }
        .sidebar { width: 250px; flex-shrink: 0; }
        .main-content { flex-grow: 1; }
        
        /* Forms */
        .form-container { max-width: 500px; margin: 0 auto; background: var(--surface); padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 600; }
        .form-group input, .form-group select { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 0.5rem; }
    </style>
</head>
<body>
    <header>
        <a href="/" class="logo">CodeAlpha Store</a>
        <div class="nav-links">
            {% if request.user.is_authenticated %}
                <span>Hello, {{ request.user.username }}</span>
                <a href="{% url 'store:logout' %}">Logout</a>
            {% else %}
                <a href="{% url 'store:login' %}">Login</a>
                <a href="{% url 'store:register' %}" class="btn">Register</a>
            {% endif %}
            <a href="{% url 'store:cart_detail' %}" class="btn">
                Cart ({{ cart|length }})
            </a>
        </div>
    </header>
    <div class="container">
        {% if messages %}
            {% for message in messages %}
                <div class="messages {{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>""",

    "store/product/list.html": """{% extends "store/base.html" %}
{% load static %}
{% block title %}
  {% if category %}{{ category.name }}{% else %}Products{% endif %}
{% endblock %}
{% block content %}
<div class="flex-row">
    <div class="sidebar">
        <h3>Categories</h3>
        <ul style="list-style:none; margin-top:1rem; display:flex; flex-direction:column; gap:0.5rem;">
            <li><a href="{% url 'store:product_list' %}" style="{% if not category %}font-weight:bold; color:var(--primary-color){% endif %}">All</a></li>
            {% for c in categories %}
                <li><a href="{{ c.get_absolute_url }}" style="{% if category.slug == c.slug %}font-weight:bold; color:var(--primary-color){% endif %}">{{ c.name }}</a></li>
            {% endfor %}
        </ul>
    </div>
    <div class="main-content">
        <h1 style="margin-bottom: 2rem;">{% if category %}{{ category.name }}{% else %}All Products{% endif %}</h1>
        <div class="product-grid">
            {% for product in products %}
                <div class="product-card">
                    <a href="{{ product.get_absolute_url }}">
                        {% if product.image %}
                            <img src="{{ product.image.url }}" class="product-img">
                        {% else %}
                            <div class="product-img" style="display:flex; align-items:center; justify-content:center; color:#94a3b8;">No Image</div>
                        {% endif %}
                    </a>
                    <div class="product-info">
                        <h3><a href="{{ product.get_absolute_url }}">{{ product.name }}</a></h3>
                        <div class="product-price">${{ product.price }}</div>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}""",

    "store/product/detail.html": """{% extends "store/base.html" %}
{% block title %}{{ product.name }}{% endblock %}
{% block content %}
<div class="flex-row" style="background:var(--surface); padding:2rem; border-radius:1rem; box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);">
    <div style="flex:1;">
        {% if product.image %}
            <img src="{{ product.image.url }}" style="width:100%; border-radius:1rem;">
        {% else %}
            <div style="width:100%; height:400px; background:#e2e8f0; border-radius:1rem; display:flex; align-items:center; justify-content:center;">No Image</div>
        {% endif %}
    </div>
    <div style="flex:1; display:flex; flex-direction:column; gap:1.5rem;">
        <h1>{{ product.name }}</h1>
        <div style="font-size:2rem; font-weight:700; color:var(--primary-color);">${{ product.price }}</div>
        <p style="color:var(--text-muted); line-height:1.8;">{{ product.description }}</p>
        <form action="{% url 'store:cart_add' product.id %}" method="post" style="display:flex; gap:1rem; align-items:center;">
            {% csrf_token %}
            {{ cart_product_form.as_p }}
            <input type="submit" value="Add to cart" class="btn" style="padding:0.75rem 2rem; font-size:1.1rem;">
        </form>
    </div>
</div>
{% endblock %}""",

    "store/cart/detail.html": """{% extends "store/base.html" %}
{% block title %}Your Shopping Cart{% endblock %}
{% block content %}
<div style="background:var(--surface); padding:2rem; border-radius:1rem; box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);">
    <h1 style="margin-bottom: 2rem;">Your Shopping Cart</h1>
    <table style="width:100%; border-collapse: collapse; margin-bottom:2rem;">
        <thead style="border-bottom:2px solid var(--border); text-align:left;">
            <tr>
                <th style="padding:1rem;">Product</th>
                <th style="padding:1rem;">Quantity</th>
                <th style="padding:1rem;">Unit Price</th>
                <th style="padding:1rem;">Total</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            {% for item in cart %}
                {% with product=item.product %}
                <tr style="border-bottom:1px solid var(--border);">
                    <td style="padding:1rem;">{{ product.name }}</td>
                    <td style="padding:1rem;">
                        <form action="{% url 'store:cart_add' product.id %}" method="post" style="display:flex; gap:0.5rem;">
                            {% csrf_token %}
                            {{ item.update_quantity_form.quantity }}
                            {{ item.update_quantity_form.override }}
                            <input type="submit" value="Update" class="btn" style="padding:0.25rem 0.5rem; font-size:0.9rem;">
                        </form>
                    </td>
                    <td style="padding:1rem;">${{ item.price }}</td>
                    <td style="padding:1rem; font-weight:bold;">${{ item.total_price }}</td>
                    <td style="padding:1rem;">
                        <form action="{% url 'store:cart_remove' product.id %}" method="post">
                            {% csrf_token %}
                            <input type="submit" value="Remove" style="color:#ef4444; background:none; border:none; cursor:pointer; font-weight:600;">
                        </form>
                    </td>
                </tr>
                {% endwith %}
            {% empty %}
                <tr><td colspan="5" style="padding:2rem; text-align:center; color:var(--text-muted);">Your cart is empty.</td></tr>
            {% endfor %}
        </tbody>
    </table>
    
    {% if cart|length > 0 %}
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <a href="{% url 'store:product_list' %}" class="btn" style="background:var(--text-muted);">Continue Shopping</a>
            <div style="display:flex; gap:2rem; align-items:center;">
                <h3 style="font-size:1.5rem;">Total: ${{ cart.get_total_price }}</h3>
                <a href="{% url 'store:order_create' %}" class="btn" style="padding:1rem 2rem; font-size:1.1rem;">Checkout</a>
            </div>
        </div>
    {% endif %}
</div>
{% endblock %}""",

    "store/order/create.html": """{% extends "store/base.html" %}
{% block title %}Checkout{% endblock %}
{% block content %}
<div class="flex-row">
    <div class="form-container" style="flex:2;">
        <h2>Shipping Information</h2>
        <form method="post" style="margin-top:1.5rem;">
            {% csrf_token %}
            {% for field in form %}
                <div class="form-group">
                    <label>{{ field.label }}</label>
                    {{ field }}
                </div>
            {% endfor %}
            <input type="submit" value="Place Order" class="btn" style="width:100%; padding:1rem; margin-top:1rem; font-size:1.1rem;">
        </form>
    </div>
    <div style="flex:1; background:var(--surface); padding:2rem; border-radius:1rem; height:fit-content; box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);">
        <h3 style="margin-bottom:1rem;">Order Summary</h3>
        <ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; border-bottom:1px solid var(--border); padding-bottom:1rem; margin-bottom:1rem;">
            {% for item in cart %}
                <li style="display:flex; justify-content:space-between;">
                    <span>{{ item.quantity }}x {{ item.product.name }}</span>
                    <span>${{ item.total_price }}</span>
                </li>
            {% endfor %}
        </ul>
        <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:1.25rem;">
            <span>Total</span>
            <span>${{ cart.get_total_price }}</span>
        </div>
    </div>
</div>
{% endblock %}""",

    "store/order/created.html": """{% extends "store/base.html" %}
{% block title %}Order Created{% endblock %}
{% block content %}
<div style="text-align:center; padding:4rem 2rem; background:var(--surface); border-radius:1rem; box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);">
    <h1 style="color:#10b981; margin-bottom:1rem;">Thank you!</h1>
    <p style="font-size:1.25rem; color:var(--text-muted); margin-bottom:2rem;">Your order has been successfully completed. Your order number is <strong>{{ order.id }}</strong>.</p>
    <a href="{% url 'store:product_list' %}" class="btn">Continue Shopping</a>
</div>
{% endblock %}""",

    "store/auth/login.html": """{% extends "store/base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="form-container">
    <h2 style="margin-bottom: 1.5rem; text-align:center;">Login to your account</h2>
    <form method="POST">
        {% csrf_token %}
        {{ login_form.as_p }}
        <button class="btn" type="submit" style="width:100%; margin-top:1rem;">Login</button>
    </form>
    <p style="margin-top:1.5rem; text-align:center; color:var(--text-muted);">
        Don't have an account? <a href="{% url 'store:register' %}" style="color:var(--primary-color);">Register here</a>.
    </p>
</div>
{% endblock %}""",

    "store/auth/register.html": """{% extends "store/base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<div class="form-container">
    <h2 style="margin-bottom: 1.5rem; text-align:center;">Create an account</h2>
    <form method="POST">
        {% csrf_token %}
        {{ register_form.as_p }}
        <button class="btn" type="submit" style="width:100%; margin-top:1rem;">Register</button>
    </form>
    <p style="margin-top:1.5rem; text-align:center; color:var(--text-muted);">
        Already have an account? <a href="{% url 'store:login' %}" style="color:var(--primary-color);">Login here</a>.
    </p>
</div>
{% endblock %}"""
}

for path, content in templates.items():
    full_path = os.path.join(BASE_DIR, *path.split('/'))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Templates created successfully!")
