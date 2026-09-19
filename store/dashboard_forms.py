from django import forms
from .models import UserProfile, Product, Category, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'stock', 'available', 'featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'payment_status']

from django.contrib.auth.models import User

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AdminUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_photo']
