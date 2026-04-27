from django.contrib import admin
from .models import Category, Product, Order, OrderItem, CartItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['id','name','phone','total','payment_type','payment_status','status','created_at']
    list_filter   = ['payment_type','payment_status','status']
    list_editable = ['payment_status','status']
    search_fields = ['name','phone','upi_ref']
    inlines       = [OrderItemInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name','category','price','stock']
    list_editable = ['price','stock']
    list_filter   = ['category']

admin.site.register(Category)
