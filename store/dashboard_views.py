from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
import json
from .models import Product, Category, Order, Review, StoreActivity
from django.contrib.auth.models import User
from .dashboard_forms import ProductForm, CategoryForm, OrderStatusForm
from django.core.paginator import Paginator

def is_store_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Store Manager').exists())

@user_passes_test(is_store_admin, login_url='/login/')
def dashboard_home(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    total_customers = User.objects.filter(is_staff=False).count()
    low_stock = Product.objects.filter(stock__lt=5).count()
    
    total_revenue = Order.objects.filter(payment_status='Completed').aggregate(Sum('final_total'))['final_total__sum'] or 0
    
    recent_orders = Order.objects.order_by('-created')[:5]
    recent_products = Product.objects.order_by('-created')[:5]
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_customers': total_customers,
        'low_stock': low_stock,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
    }
    return render(request, 'dashboard/home.html', context)

# Products
@user_passes_test(is_store_admin, login_url='/login/')
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all().order_by('-created')
    if query:
        products = products.filter(name__icontains=query)
        
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/product_list.html', {'page_obj': page_obj, 'query': query})

@user_passes_test(is_store_admin, login_url='/login/')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if isinstance(form.instance, Product):
                StoreActivity.objects.create(event_type='admin', user=request.user, product=form.instance, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} product {form.instance.name}")
            elif isinstance(form.instance, Category):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} category {form.instance.name}")
            elif isinstance(form.instance, Order):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"Updated status for order {form.instance.order_number}")
            messages.success(request, 'Product created successfully.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add Product'})

@user_passes_test(is_store_admin, login_url='/login/')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            if isinstance(form.instance, Product):
                StoreActivity.objects.create(event_type='admin', user=request.user, product=form.instance, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} product {form.instance.name}")
            elif isinstance(form.instance, Category):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} category {form.instance.name}")
            elif isinstance(form.instance, Order):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"Updated status for order {form.instance.order_number}")
            messages.success(request, 'Product updated successfully.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})

@user_passes_test(is_store_admin, login_url='/login/')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        StoreActivity.objects.create(event_type='admin', user=request.user, description=f"Deleted product {product.name}")
        messages.success(request, 'Product deleted successfully.')
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': product, 'title': 'Delete Product', 'cancel_url': 'dashboard:product_list'})

# Categories
@user_passes_test(is_store_admin, login_url='/login/')
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'dashboard/category_list.html', {'categories': categories})

@user_passes_test(is_store_admin, login_url='/login/')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if isinstance(form.instance, Product):
                StoreActivity.objects.create(event_type='admin', user=request.user, product=form.instance, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} product {form.instance.name}")
            elif isinstance(form.instance, Category):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} category {form.instance.name}")
            elif isinstance(form.instance, Order):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"Updated status for order {form.instance.order_number}")
            messages.success(request, 'Category created successfully.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add Category'})

@user_passes_test(is_store_admin, login_url='/login/')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            if isinstance(form.instance, Product):
                StoreActivity.objects.create(event_type='admin', user=request.user, product=form.instance, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} product {form.instance.name}")
            elif isinstance(form.instance, Category):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} category {form.instance.name}")
            elif isinstance(form.instance, Order):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"Updated status for order {form.instance.order_number}")
            messages.success(request, 'Category updated successfully.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Edit Category'})

@user_passes_test(is_store_admin, login_url='/login/')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        if category.products.exists():
            messages.error(request, 'Cannot delete category because it contains products.')
            return redirect('dashboard:category_list')
        category.delete()
        StoreActivity.objects.create(event_type='admin', user=request.user, description=f"Deleted category {category.name}")
        messages.success(request, 'Category deleted successfully.')
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': category, 'title': 'Delete Category', 'cancel_url': 'dashboard:category_list'})

# Orders
@user_passes_test(is_store_admin, login_url='/login/')
def order_list(request):
    status_filter = request.GET.get('status', '')
    orders = Order.objects.all().order_by('-created')
    if status_filter:
        orders = orders.filter(status=status_filter)
        
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/order_list.html', {'page_obj': page_obj, 'status_filter': status_filter})

@user_passes_test(is_store_admin, login_url='/login/')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            if isinstance(form.instance, Product):
                StoreActivity.objects.create(event_type='admin', user=request.user, product=form.instance, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} product {form.instance.name}")
            elif isinstance(form.instance, Category):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"{'Created' if not hasattr(form.instance, '_pre_save_id') else 'Updated'} category {form.instance.name}")
            elif isinstance(form.instance, Order):
                StoreActivity.objects.create(event_type='admin', user=request.user, description=f"Updated status for order {form.instance.order_number}")
            messages.success(request, 'Order updated successfully.')
            return redirect('dashboard:order_detail', pk=pk)
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'dashboard/order_detail.html', {'order': order, 'form': form})

# Reviews
@user_passes_test(is_store_admin, login_url='/login/')
def review_list(request):
    reviews = Review.objects.all().order_by('-created')
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/review_list.html', {'page_obj': page_obj})

@user_passes_test(is_store_admin, login_url='/login/')
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        StoreActivity.objects.create(event_type='admin', user=request.user, description=f"Deleted review by {review.user.username}")
        messages.success(request, 'Review deleted successfully.')
        return redirect('dashboard:review_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': review, 'title': 'Delete Review', 'cancel_url': 'dashboard:review_list'})

# Analytics & Activity
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
import json

@user_passes_test(is_store_admin, login_url='/login/')
def dashboard_analytics(request):
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Base querysets
    activities = StoreActivity.objects.filter(created__gte=start_date)
    orders = Order.objects.filter(created__gte=start_date)
    
    # CUSTOMERS
    total_customers = User.objects.filter(is_staff=False).count()
    new_customers = User.objects.filter(is_staff=False, date_joined__gte=start_date).count()
    
    # PRODUCTS
    total_views = activities.filter(event_type='view').count()
    most_viewed = Product.objects.annotate(views=Count('activities', filter=models.Q(activities__event_type='view', activities__created__gte=start_date))).order_by('-views')[:5]
    most_carted = Product.objects.annotate(carts=Count('activities', filter=models.Q(activities__event_type='cart', activities__created__gte=start_date))).order_by('-carts')[:5]
    most_wishlisted = Product.objects.annotate(wishes=Count('activities', filter=models.Q(activities__event_type='wishlist', activities__created__gte=start_date))).order_by('-wishes')[:5]
    
    # SALES
    period_orders = orders.count()
    period_revenue = orders.filter(payment_status='Completed').aggregate(Sum('final_total'))['final_total__sum'] or 0
    
    # --- CHART DATA ---
    # 1. Trend Chart
    trend_qs = orders.filter(payment_status='Completed').annotate(date=TruncDate('created')).values('date').annotate(
        revenue=Sum('final_total'),
        count=Count('id')
    ).order_by('date')
    
    trend_dict = {item['date'].strftime('%Y-%m-%d'): item for item in trend_qs if item['date']}
    
    trend_labels = []
    trend_revenue = []
    trend_orders = []
    
    current_date = start_date.date()
    end_date = timezone.now().date()
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        trend_labels.append(date_str)
        if date_str in trend_dict:
            trend_revenue.append(float(trend_dict[date_str]['revenue']))
            trend_orders.append(trend_dict[date_str]['count'])
        else:
            trend_revenue.append(0.0)
            trend_orders.append(0)
        current_date += timedelta(days=1)
        
    # 2. Category Performance Chart
    category_views = Category.objects.annotate(
        views=Count('products__activities', filter=models.Q(products__activities__event_type='view', products__activities__created__gte=start_date))
    ).filter(views__gt=0).order_by('-views')
    
    cat_labels = [c.name for c in category_views]
    cat_data = [c.views for c in category_views]

    # 3. Product Performance Chart
    top_products = Product.objects.annotate(
        views=Count('activities', filter=models.Q(activities__event_type='view', activities__created__gte=start_date)),
        carts=Count('activities', filter=models.Q(activities__event_type='cart', activities__created__gte=start_date))
    ).filter(models.Q(views__gt=0) | models.Q(carts__gt=0)).order_by('-views')[:10]
    
    prod_labels = [p.name[:15] + '...' if len(p.name) > 15 else p.name for p in top_products]
    prod_views = [p.views for p in top_products]
    prod_carts = [p.carts for p in top_products]
    
    context = {
        'days': days,
        'total_customers': total_customers,
        'new_customers': new_customers,
        'total_views': total_views,
        'most_viewed': most_viewed,
        'most_carted': most_carted,
        'most_wishlisted': most_wishlisted,
        'period_orders': period_orders,
        'period_revenue': period_revenue,
        
        # JSON strings for JS
        'trend_labels': json.dumps(trend_labels),
        'trend_revenue': json.dumps(trend_revenue),
        'trend_orders': json.dumps(trend_orders),
        'cat_labels': json.dumps(cat_labels),
        'cat_data': json.dumps(cat_data),
        'prod_labels': json.dumps(prod_labels),
        'prod_views': json.dumps(prod_views),
        'prod_carts': json.dumps(prod_carts),
    }
    return render(request, 'dashboard/analytics.html', context)

@user_passes_test(is_store_admin, login_url='/login/')
def dashboard_activity(request):
    activities = StoreActivity.objects.filter(event_type='admin').select_related('user', 'product').order_by('-created')
    paginator = Paginator(activities, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/activity.html', {'page_obj': page_obj})

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .dashboard_forms import AdminProfileForm



from .models import UserProfile
from .dashboard_forms import AdminProfileForm, AdminUserProfileForm

@user_passes_test(is_store_admin, login_url='/login/')
def admin_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = AdminProfileForm(request.POST, instance=user)
        profile_form = AdminUserProfileForm(request.POST, request.FILES, instance=profile)
        
        # Handle remove photo
        if 'remove_photo' in request.POST:
            if profile.profile_photo:
                profile.profile_photo.delete()
                profile.profile_photo = None
                profile.save()
                StoreActivity.objects.create(event_type='admin', user=user, description="Removed profile photo")
                messages.success(request, 'Profile photo removed successfully.')
                return redirect('dashboard:profile')
                
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            StoreActivity.objects.create(event_type='admin', user=user, description="Updated profile information")
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard:profile')
    else:
        user_form = AdminProfileForm(instance=user)
        profile_form = AdminUserProfileForm(instance=profile)

    return render(request, 'dashboard/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    })

@user_passes_test(is_store_admin, login_url='/login/')
def admin_password_change(request):
    user = request.user
    
    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep logged in
            StoreActivity.objects.create(event_type='admin', user=user, description="Changed password")
            messages.success(request, 'Password changed successfully.')
            return redirect('dashboard:password_change')
    else:
        password_form = PasswordChangeForm(user)

    return render(request, 'dashboard/password_change.html', {
        'password_form': password_form
    })
