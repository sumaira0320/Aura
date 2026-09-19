from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Category, Product, OrderItem, Order, Review, StoreActivity
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm, ReviewForm
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created')
    else:  # featured or default
        products = products.order_by('-featured', '-created')
        
    featured_products = products.filter(featured=True)[:5] if not category and not query and not request.GET.get('sort') else None
    
    paginator = Paginator(products, 12) # 12 products per page (matches 4-column grid)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
        
    return render(request, 'store/product/list.html', {
        'category': category,
        'categories': categories,
        'products': page_obj,
        'featured_products': featured_products,
        'query': query,
        'sort': sort,
        'page_obj': page_obj
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    # Track Product View
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key
    
    user = request.user if request.user.is_authenticated else None
    StoreActivity.objects.create(
        event_type='view',
        product=product,
        user=user,
        session_key=session_key
    )

    cart_product_form = CartAddProductForm()
    
    # Handle reviews
    reviews = product.reviews.all()
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('store:product_detail', id=product.id, slug=product.slug)
    else:
        review_form = ReviewForm()
        
    # Related products
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    
    return render(request, 'store/product/detail.html', {
        'product': product, 
        'cart_product_form': cart_product_form,
        'reviews': reviews,
        'review_form': review_form,
        'related_products': related_products
    })

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        requested_qty = cd['quantity']
        
        # Calculate resulting quantity based on override vs addition
        if cd['override']:
            new_qty = requested_qty
        else:
            product_id_str = str(product.id)
            current_qty = cart.cart.get(product_id_str, {}).get('quantity', 0)
            new_qty = current_qty + requested_qty
            
        if not product.available:
            messages.error(request, f"{product.name} is currently unavailable.")
        elif new_qty > product.stock:
            messages.error(request, f"Cannot add {new_qty} of {product.name} to cart. Only {product.stock} available.")
        else:
            cart.add(product=product, quantity=requested_qty, override_quantity=cd['override'])
            messages.success(request, f"Updated {product.name} in your cart.")
            
            # Track Add to Cart
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            user = request.user if request.user.is_authenticated else None
            StoreActivity.objects.create(
                event_type='cart',
                product=product,
                user=user,
                session_key=session_key
            )
    else:
        messages.error(request, "Invalid quantity provided.")
    return redirect('store:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"Removed {product.name} from your cart.")
    return redirect('store:cart_detail')
    
@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Your cart has been cleared.")
    return redirect('store:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        # Pass product stock as max_value to the form dynamically
        form = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
        form.fields['quantity'].widget.attrs['max'] = item['product'].stock
        item['update_quantity_form'] = form
    return render(request, 'store/cart/detail.html', {'cart': cart})

from django.db import transaction

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('store:cart_detail')
        
    # Configurable shipping rules
    subtotal = cart.get_total_price()
    shipping_cost = 0 if subtotal > 100 else 15
    final_total = subtotal + shipping_cost

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        payment_method = request.POST.get('payment_method')
        
        if payment_method != 'demo':
            messages.error(request, "Please select Demo Payment.")
        elif form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    order.shipping_cost = shipping_cost
                    order.final_total = final_total
                    order.status = 'Pending'
                    order.payment_status = 'Completed' # Demo payment is instantly completed
                    order.save()
                    
                    # Track Order Placed
                    session_key = request.session.session_key
                    user = request.user if request.user.is_authenticated else None
                    StoreActivity.objects.create(
                        event_type='order',
                        user=user,
                        session_key=session_key,
                        description=f"Order {order.order_number} placed for ${order.final_total}"
                    )
                    
                    for item in cart:
                        product = item['product']
                        # Re-check stock in DB to avoid stale data
                        product.refresh_from_db()
                        if product.stock < item['quantity']:
                            raise ValueError(f"Not enough stock for {product.name}. Only {product.stock} left.")
                            
                        # Reduce stock safely
                        product.stock -= item['quantity']
                        if product.stock == 0:
                            product.available = False
                        product.save()
                        
                        OrderItem.objects.create(
                            order=order, 
                            product=product, 
                            price=item['price'], 
                            quantity=item['quantity']
                        )
                    cart.clear()
                    return render(request, 'store/order/created.html', {'order': order})
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('store:cart_detail')
    else:
        # Pre-fill with user info if logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)
        
    return render(request, 'store/order/create.html', {
        'cart': cart, 
        'form': form,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'final_total': final_total
    })
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order/history.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'store/order/detail.html', {'order': order})
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegistrationForm, UserEditForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:profile')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome to Aura!")
            return redirect('store:product_list')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, "store/auth/register.html", {"register_form": form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name='Store Manager').exists():
            return redirect('dashboard:home')
        return redirect('store:profile')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                
                if user.is_superuser or user.groups.filter(name='Store Manager').exists():
                    return redirect('dashboard:home')
                
                # Check for next param
                next_url = request.GET.get('next', 'store:profile')
                if not next_url.startswith('/'):
                    next_url = 'store:profile'
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "store/auth/login.html", {"login_form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out. See you soon!") 
    return redirect('store:product_list')

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    reviews = Review.objects.filter(user=request.user).order_by('-created')
    wishlist_count = Product.objects.filter(users_wishlist=request.user).count()
    
    context = {
        'orders_count': orders.count(),
        'reviews_count': reviews.count(),
        'wishlist_count': wishlist_count,
        'recent_orders': orders[:3],
        'recent_reviews': reviews[:3],
    }
    return render(request, 'store/profile/dashboard.html', context)

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('store:profile')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'store/profile/edit.html', {'form': form})

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect('store:profile')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'store/profile/password_change.html', {'form': form})

@login_required
def wishlist_view(request):
    wishlist_products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'store/profile/wishlist.html', {'wishlist_products': wishlist_products})

@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, f"{product.name} removed from your wishlist.")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, f"{product.name} added to your wishlist.")
        
        # Track Wishlist Add
        StoreActivity.objects.create(
            event_type='wishlist',
            product=product,
            user=request.user
        )
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))
