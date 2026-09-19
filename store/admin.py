from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Category, Product, Order, OrderItem, Review

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True)
        return qs
        
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            # Remove 'Permissions' section to prevent privilege escalation
            fieldsets = tuple(fs for fs in fieldsets if fs[0] != 'Permissions')
        return fieldsets

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and obj and obj.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser and obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser
        
    def has_add_permission(self, request):
        return request.user.is_superuser
        
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
        
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created']
    list_filter = ['rating', 'created']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'featured', 'created', 'updated']
    list_filter = ['available', 'featured', 'created', 'updated']
    list_editable = ['price', 'stock', 'available', 'featured']
    prepopulated_fields = {'slug': ('name',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'email', 'status', 'payment_status', 'final_total', 'created']
    list_filter = ['status', 'payment_status', 'created', 'updated']
    list_editable = ['status', 'payment_status']
    search_fields = ['order_number', 'first_name', 'last_name', 'email']
    inlines = [OrderItemInline]
