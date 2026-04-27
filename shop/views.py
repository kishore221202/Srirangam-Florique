from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from decimal import Decimal
import urllib.parse

from .models import Category, Product, Order, OrderItem, CartItem

# ─── helpers ───────────────────────────────────────────────
def _sk(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _cart_count(request):
    return CartItem.objects.filter(session_key=_sk(request)).count()

def _build_wa(order):
    items = order.items.select_related('product').all()
    pay_label = dict(Order.PAYMENT_TYPE).get(order.payment_type, order.payment_type)
    lines = [
        "🌸 *NG Srirangam Flower Shop*",
        f"📋 Order #{order.id}",
        f"👤 {order.name}  |  📞 {order.phone}",
        f"📍 {order.address}", "",
        "🛒 *Items:*",
    ]
    for it in items:
        lines.append(f"  • {it.product.name}  ×{it.quantity}  = ₹{it.subtotal()}")
    lines += ["", f"💰 *Total: ₹{order.total}*",
              f"💳 Payment: {pay_label}"]
    if order.payment_type == 'advance':
        lines += [f"✅ Advance: ₹{order.advance_amount}",
                  f"⏳ Balance: ₹{order.balance_amount}"]
    if order.payment_type == 'upi' and order.upi_ref:
        lines.append(f"🔖 UPI Ref: {order.upi_ref}")
    if order.notes:
        lines.append(f"📝 {order.notes}")
    lines.append("\nThank you! 🙏")
    return "\n".join(lines)

# ─── views ─────────────────────────────────────────────────
def index(request):
    categories = Category.objects.all()
    cat_slug   = request.GET.get('cat', '')
    products   = Product.objects.filter(category__slug=cat_slug) if cat_slug \
                 else Product.objects.all()
    return render(request, 'shop/index.html', {
        'products': products, 'categories': categories,
        'selected_cat': cat_slug, 'cart_count': _cart_count(request),
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {
        'product': product, 'cart_count': _cart_count(request),
    })

def add_to_cart(request, pk):
    sk      = _sk(request)
    product = get_object_or_404(Product, pk=pk)
    item, created = CartItem.objects.get_or_create(session_key=sk, product=product)
    if not created:
        item.quantity += 1; item.save()
    count = CartItem.objects.filter(session_key=sk).count()
    return JsonResponse({'status': 'ok', 'count': count, 'product': product.name})

def remove_from_cart(request, pk):
    CartItem.objects.filter(session_key=_sk(request), product_id=pk).delete()
    return redirect('cart')

def update_cart(request, pk):
    sk  = _sk(request)
    qty = int(request.POST.get('quantity', 1))
    item = get_object_or_404(CartItem, session_key=sk, product_id=pk)
    if qty < 1: item.delete()
    else: item.quantity = qty; item.save()
    return redirect('cart')

def cart(request):
    sk    = _sk(request)
    items = CartItem.objects.filter(session_key=sk).select_related('product')
    total   = sum(i.subtotal() for i in items)
    advance = round(total * Decimal('0.5'), 2)
    return render(request, 'shop/cart.html', {
        'items': items, 'total': total, 'advance': advance,
        'cart_count': items.count(),
    })

def checkout(request):
    sk    = _sk(request)
    items = CartItem.objects.filter(session_key=sk).select_related('product')
    if not items.exists():
        return redirect('index')

    total   = sum(i.subtotal() for i in items)
    advance = round(total * Decimal('0.5'), 2)
    balance = total - advance

    if request.method == 'POST':
        name         = request.POST['name']
        phone        = request.POST['phone']
        address      = request.POST['address']
        notes        = request.POST.get('notes', '')
        payment_type = request.POST.get('payment_type', 'cash')

        if payment_type == 'advance':
            adv_amt = advance; bal_amt = balance
        else:
            adv_amt = total;   bal_amt = Decimal('0')

        order = Order.objects.create(
            name=name, phone=phone, address=address, notes=notes,
            total=total, advance_amount=adv_amt, balance_amount=bal_amt,
            payment_type=payment_type,
            payment_status='pending',
        )
        for i in items:
            OrderItem.objects.create(order=order, product=i.product,
                                     quantity=i.quantity, price=i.product.price)
        items.delete()

        # Go to payment page
        return redirect('payment', order_id=order.id)

    return render(request, 'shop/checkout.html', {
        'items': items, 'total': total, 'advance': advance, 'balance': balance,
        'cart_count': items.count(),
    })

def payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    upi_id   = getattr(settings, 'SHOP_UPI_ID',   'yourname@upi')
    upi_name = getattr(settings, 'SHOP_UPI_NAME',  'NG Flower Shop')

    # Amount to pay now
    pay_now = order.advance_amount if order.payment_type == 'advance' else order.total

    # UPI deep link (works on mobile)
    upi_link = (f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(upi_name)}"
                f"&am={pay_now}&cu=INR&tn=Order{order.id}")

    # Google Pay / PhonePe / Paytm QR string (same UPI link)
    upi_qr_data = upi_link

    bank = {
        'name':   getattr(settings, 'SHOP_BANK_NAME',   'SBI'),
        'acc':    getattr(settings, 'SHOP_BANK_ACC',    '0000000000'),
        'ifsc':   getattr(settings, 'SHOP_BANK_IFSC',   'SBIN0000000'),
        'holder': getattr(settings, 'SHOP_BANK_HOLDER', 'NG Flower Shop'),
    }

    if request.method == 'POST':
        upi_ref = request.POST.get('upi_ref', '').strip()
        action  = request.POST.get('action', '')

        if action == 'confirm_upi':
            order.upi_ref        = upi_ref
            order.payment_status = 'paid' if upi_ref else 'pending'
            order.save()
        elif action == 'confirm_cash':
            order.payment_status = 'pending'   # cash = pay at delivery
            order.save()
        elif action == 'confirm_advance':
            order.upi_ref        = upi_ref
            order.payment_status = 'advance_paid'
            order.save()
        elif action == 'confirm_netbank':
            order.upi_ref        = upi_ref
            order.payment_status = 'paid'
            order.save()

        # WhatsApp redirect
        wa_msg = _build_wa(order)
        wa_num = getattr(settings, 'WHATSAPP_NUMBER', '919876543210')
        wa_url = f"https://wa.me/{wa_num}?text={urllib.parse.quote(wa_msg)}"
        return render(request, 'shop/order_success.html', {
            'order': order, 'wa_url': wa_url, 'cart_count': 0,
        })

    return render(request, 'shop/payment.html', {
        'order':       order,
        'pay_now':     pay_now,
        'upi_id':      upi_id,
        'upi_link':    upi_link,
        'upi_qr_data': upi_qr_data,
        'bank':        bank,
        'cart_count':  0,
    })

def order_history(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'shop/order_history.html', {
        'orders': orders, 'cart_count': _cart_count(request),
    })
