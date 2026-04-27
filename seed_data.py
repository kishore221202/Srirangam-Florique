"""python seed_data.py"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowershop.settings')
django.setup()
from shop.models import Category, Product

Product.objects.all().delete()
Category.objects.all().delete()

cat = Category.objects.create(name='Garlands', icon='🌿', slug='garlands')

products = [
    ('Rose Malai – ரோஜா மாலை', 180),
    ('Jasmine Malai – மல்லிகை மாலை', 120),
    ('Marigold Malai – சாமந்தி மாலை', 60),
    ('Mixed Flower Malai – கலப்பு பூ மாலை', 150),
    ('Lotus Malai – தாமரை மாலை', 200),
    ('Orchid Malai – ஆர்கிட் மாலை', 300),
    ('Julaippu Malai – ஜுலைப்பு மாலை', 90),
    ('Akkamalai – அக்கமாலை', 110),
    ('Neem Malai – வேப்பிலை மாலை', 70),
    ('Tulsi Malai – துளசி மாலை', 80),
    ('Theme Malai – தீம் மாலை', 250),
    ('Beads Malai – முத்து மாலை', 220),
    ('Artificial Malai – செயற்கை மாலை', 140),
    ('Money Malai – பணம் மாலை', 500),
    ('Chocolate Malai – சாக்லேட் மாலை', 300),
    ('Coin Malai – நாணயம் மாலை', 260),
    ('Thodutha Malai – கட்டிய மாலை', 100),
]

for name, price in products:
    Product.objects.create(
        category=cat, name=name,
        description='Fresh & Handmade', price=price,
        emoji='🌸', bg_class='bg-pink', badge='New',
    )
    print('Added:', name)
print('✅ Done!')
