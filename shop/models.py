from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='🌸')
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    name        = models.CharField(max_length=200)
    description = models.TextField(default='Fresh & Handmade')
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    emoji       = models.CharField(max_length=10, default='🌸')
    bg_class    = models.CharField(max_length=50, default='bg-pink')
    badge       = models.CharField(max_length=50, blank=True)
    stock       = models.IntegerField(default=100)
    image       = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url   = models.URLField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

    def get_image(self):
        if self.image:   return self.image.url
        if self.image_url: return self.image_url
        return None

class Order(models.Model):
    # Payment type
    PAYMENT_TYPE = [
        ('upi',     'UPI / QR Code'),
        ('cash',    'Cash on Delivery'),
        ('netbank', 'Net Banking'),
        ('advance', 'Advance (50%) + Balance'),
    ]
    # Payment status
    PAY_STATUS = [
        ('pending',   'Payment Pending'),
        ('advance_paid', 'Advance Paid'),
        ('paid',      'Fully Paid'),
        ('failed',    'Payment Failed'),
    ]
    # Order status
    ORDER_STATUS = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    name             = models.CharField(max_length=200)
    phone            = models.CharField(max_length=15)
    address          = models.TextField()
    notes            = models.TextField(blank=True)

    total            = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_type     = models.CharField(max_length=20, choices=PAYMENT_TYPE, default='cash')
    payment_status   = models.CharField(max_length=20, choices=PAY_STATUS, default='pending')

    # UPI transaction ref (customer fills in)
    upi_ref          = models.CharField(max_length=100, blank=True, help_text='UPI Transaction ID')

    status           = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Order #{self.id} – {self.name}"
    def get_pay_now(self):
        """Amount customer needs to pay right now"""
        if self.payment_type == 'advance':
            return self.advance_amount
        elif self.payment_type == 'cash':
            return self.total          # Pay at delivery
        return self.total

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price    = models.DecimalField(max_digits=8, decimal_places=2)
    def subtotal(self): return self.price * self.quantity

class CartItem(models.Model):
    session_key = models.CharField(max_length=40)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=1)
    def subtotal(self): return self.product.price * self.quantity
