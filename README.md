# 🌸 NG Srirangam Flower Shop — Payment System

## ✨ Payment Features
| Method | Details |
|---|---|
| 📱 UPI / QR Code | Google Pay, PhonePe, Paytm, BHIM — Auto QR generate |
| 💵 Cash on Delivery | Delivery-ல் cash கொடுங்க |
| 🏦 Net Banking | NEFT / IMPS / RTGS — Bank details காட்டும் |
| 💰 Advance (50%) | இப்போது 50%, balance delivery-ல் |
| 📱 WhatsApp Order | Auto message — all order + payment details |

---

## ⚡ Setup Commands

```bash
pip install django pillow
cd ng-flower-django2
python manage.py makemigrations shop
python manage.py migrate
python seed_data.py
python manage.py createsuperuser
python manage.py runserver
```

## 🌐 URLs
- Shop     → http://127.0.0.1:8000
- Admin    → http://127.0.0.1:8000/admin
- Orders   → http://127.0.0.1:8000/orders/

---

## ⚙️ Settings மாற்றுவது — `flowershop/settings.py`

```python
WHATSAPP_NUMBER = '919876543210'     # உங்கள் WhatsApp (91 + number)
SHOP_UPI_ID     = 'yourname@upi'    # UPI ID (GPay/PhonePe/Paytm)
SHOP_UPI_NAME   = 'NG Flower Shop'  # UPI display name
SHOP_BANK_NAME  = 'State Bank of India'
SHOP_BANK_ACC   = '1234567890'      # Account number
SHOP_BANK_IFSC  = 'SBIN0001234'     # IFSC code
SHOP_BANK_HOLDER= 'NG Srirangam Flower Shop'
```

## 🖼️ Product Image Upload
Admin → Products → Image field → Upload → Save

## 💳 Payment Flow
1. Customer → Cart → Checkout → Select payment method
2. **UPI**: QR scan → Transaction ID enter → Confirm
3. **Cash**: Order confirm → Pay at delivery
4. **Net Bank**: Bank details show → UTR number enter → Confirm
5. **Advance**: 50% UPI pay → Balance at delivery
6. Success page → WhatsApp button → Send order to shop
