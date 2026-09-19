from .cart import Cart
from .models import Category

def cart(request):
    return {'cart': Cart(request)}

def store_categories(request):
    return {'store_categories': Category.objects.all()}
