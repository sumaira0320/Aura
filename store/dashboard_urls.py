from django.urls import path
from . import dashboard_views as views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    
    # Reviews
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('profile/', views.admin_profile, name='profile'),
    path('change-password/', views.admin_password_change, name='password_change'),
    path('analytics/', views.dashboard_analytics, name='analytics'),
    path('activity/', views.dashboard_activity, name='activity'),
]
