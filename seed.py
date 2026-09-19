import os
import django
import urllib.request
import json
import concurrent.futures
from django.core.files.base import ContentFile
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Category, Product

# Data Definition with keywords for loremflickr
CATEGORIES = {
    'Books': [
        {'name': 'Python Crash Course', 'price': 39.95, 'desc': 'A hands-on, project-based introduction to programming.', 'keywords': 'book,python'},
        {'name': 'The Great Gatsby', 'price': 15.99, 'desc': 'The classic novel of the Jazz Age by F. Scott Fitzgerald.', 'keywords': 'book,novel'},
        {'name': 'Clean Code', 'price': 45.00, 'desc': 'A Handbook of Agile Software Craftsmanship.', 'keywords': 'book,programming'},
        {'name': 'Atomic Habits', 'price': 24.00, 'desc': 'An Easy & Proven Way to Build Good Habits & Break Bad Ones.', 'keywords': 'book,habits'},
        {'name': 'The Pragmatic Programmer', 'price': 49.99, 'desc': 'Your journey to mastery in software development.', 'keywords': 'book,developer'},
        {'name': 'Designing Data-Intensive Applications', 'price': 55.00, 'desc': 'The big ideas behind reliable, scalable, and maintainable systems.', 'keywords': 'book,data'},
        {'name': 'Dune', 'price': 18.95, 'desc': 'Frank Herbert’s classic masterpiece—a triumph of the imagination and one of the bestselling science fiction novels of all time.', 'keywords': 'book,scifi'},
        {'name': 'Sapiens: A Brief History of Humankind', 'price': 29.99, 'desc': 'A groundbreaking narrative of humanity’s creation and evolution.', 'keywords': 'book,history'},
        {'name': 'Deep Work', 'price': 28.00, 'desc': 'Rules for focused success in a distracted world.', 'keywords': 'book,office'}
    ],
    'Clothing': [
        {'name': "Men's Classic Leather Jacket", 'price': 199.99, 'desc': 'Genuine leather jacket with a timeless design.', 'keywords': 'leather,jacket'},
        {'name': "Women's Casual Dress", 'price': 59.99, 'desc': 'A comfortable and stylish dress for everyday wear.', 'keywords': 'dress,clothing'},
        {'name': "Premium Denim Jeans", 'price': 79.50, 'desc': 'High-quality, durable denim jeans built for comfort.', 'keywords': 'jeans,denim'},
        {'name': "Organic Cotton Hoodie", 'price': 49.99, 'desc': 'Super soft and eco-friendly organic cotton hoodie.', 'keywords': 'hoodie,clothing'},
        {'name': "Running Sneakers", 'price': 120.00, 'desc': 'Lightweight and breathable sneakers for optimal performance.', 'keywords': 'sneakers,shoes'},
        {'name': "Classic Handbag", 'price': 150.00, 'desc': 'Elegant handbag made from premium materials.', 'keywords': 'handbag,fashion'},
        {'name': "Oversized T-Shirt", 'price': 25.00, 'desc': 'Relaxed fit, ultra-soft cotton oversized t-shirt.', 'keywords': 'tshirt,clothing'},
        {'name': "Winter Beanie", 'price': 15.00, 'desc': 'Warm knit beanie for cold weather.', 'keywords': 'beanie,winter'},
        {'name': "Formal Oxford Shoes", 'price': 110.00, 'desc': 'Classic leather formal shoes for men.', 'keywords': 'oxford,shoes'},
        {'name': "Silk Scarf", 'price': 35.00, 'desc': 'Beautifully patterned pure silk scarf.', 'keywords': 'scarf,silk'}
    ],
    'Electronics': [
        {'name': 'Smartwatch Pro', 'price': 249.99, 'desc': 'Advanced smartwatch with health tracking and GPS.', 'keywords': 'smartwatch,device'},
        {'name': 'Wireless Noise-Canceling Headphones', 'price': 299.00, 'desc': 'Industry-leading noise cancellation and premium sound.', 'keywords': 'headphones,audio'},
        {'name': 'Mechanical Gaming Keyboard', 'price': 129.99, 'desc': 'RGB backlit mechanical keyboard with tactile switches.', 'keywords': 'keyboard,gaming'},
        {'name': '4K Smart TV 55-inch', 'price': 699.00, 'desc': 'Stunning 4K resolution with built-in streaming apps.', 'keywords': 'television,screen'},
        {'name': 'Ergonomic Wireless Mouse', 'price': 49.99, 'desc': 'Comfortable wireless mouse for long working hours.', 'keywords': 'mouse,computer'},
        {'name': 'Ultra-Thin Laptop', 'price': 1299.00, 'desc': 'Powerful and lightweight laptop for professionals on the go.', 'keywords': 'laptop,computer'},
        {'name': 'Smartphone X', 'price': 999.00, 'desc': 'The latest flagship smartphone with a pro-grade camera.', 'keywords': 'smartphone,phone'},
        {'name': 'Waterproof Bluetooth Speaker', 'price': 79.99, 'desc': 'Portable speaker with booming bass and rugged design.', 'keywords': 'speaker,audio'},
        {'name': 'Tablet Pro 11-inch', 'price': 799.00, 'desc': 'Versatile tablet for creativity and productivity.', 'keywords': 'tablet,device'},
        {'name': 'Noise-Isolating Earbuds', 'price': 149.00, 'desc': 'True wireless earbuds with crystal-clear audio.', 'keywords': 'earbuds,audio'}
    ],
    'Home & Kitchen': [
        {'name': 'Robot Vacuum Cleaner', 'price': 349.00, 'desc': 'Smart automated vacuum cleaner with mapping technology.', 'keywords': 'vacuum,robot'},
        {'name': 'Espresso Machine', 'price': 499.99, 'desc': 'Professional-grade espresso machine for home use.', 'keywords': 'espresso,machine'},
        {'name': 'Non-Stick Cookware Set', 'price': 149.99, 'desc': '10-piece durable non-stick pots and pans.', 'keywords': 'cookware,pans'},
        {'name': 'Digital Air Fryer', 'price': 89.99, 'desc': 'Healthy frying with less oil and digital touch controls.', 'keywords': 'kitchen,appliance'},
        {'name': 'Modern Table Lamp', 'price': 39.99, 'desc': 'Minimalist table lamp with adjustable brightness.', 'keywords': 'lamp,lighting'},
        {'name': 'Kitchen Pantry Organizer', 'price': 29.99, 'desc': 'Space-saving organizer for your kitchen cabinets.', 'keywords': 'pantry,organizer'},
        {'name': 'Standing Desk', 'price': 299.00, 'desc': 'Height-adjustable standing desk for an ergonomic workspace.', 'keywords': 'desk,office'},
        {'name': 'Ceramic Coffee Mug Set', 'price': 24.00, 'desc': 'Set of 4 artisan ceramic coffee mugs.', 'keywords': 'mug,coffee'},
        {'name': 'Memory Foam Pillow', 'price': 45.00, 'desc': 'Contoured memory foam pillow for neck support.', 'keywords': 'pillow,bed'},
        {'name': 'Blender Pro', 'price': 120.00, 'desc': 'High-speed blender for smoothies and soups.', 'keywords': 'blender,kitchen'}
    ],
    'Sports': [
        {'name': 'Adjustable Dumbbell Set', 'price': 199.99, 'desc': 'Space-saving adjustable dumbbells up to 50 lbs each.', 'keywords': 'dumbbell,fitness'},
        {'name': 'Premium Yoga Mat', 'price': 39.99, 'desc': 'Non-slip, eco-friendly yoga mat with alignment lines.', 'keywords': 'yoga,mat'},
        {'name': 'Official Size Football', 'price': 29.99, 'desc': 'High-quality leather football for professional play.', 'keywords': 'football,sports'},
        {'name': 'Indoor/Outdoor Basketball', 'price': 34.95, 'desc': 'Durable composite leather basketball.', 'keywords': 'basketball,sports'},
        {'name': 'Trail Running Shoes', 'price': 130.00, 'desc': 'Rugged shoes designed for off-road running.', 'keywords': 'running,shoes'},
        {'name': 'Resistance Bands Set', 'price': 19.99, 'desc': 'Set of 5 resistance bands for full-body workouts.', 'keywords': 'fitness,bands'},
        {'name': 'Insulated Fitness Bottle', 'price': 25.00, 'desc': 'Stainless steel bottle that keeps water cold for 24 hours.', 'keywords': 'bottle,water'},
        {'name': 'Durable Gym Bag', 'price': 45.00, 'desc': 'Spacious gym bag with a dedicated shoe compartment.', 'keywords': 'gym,bag'}
    ]
}

def generate_image_for_product(keywords):
    url = f"https://loremflickr.com/600/600/{keywords}/all"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.read()
    except Exception as e:
        print(f"Failed to fetch image for {keywords}: {e}")
        return None

def process_product(cat_name, p_data):
    category = Category.objects.get(name=cat_name)
    slug = slugify(p_data['name'])
    
    product, created = Product.objects.get_or_create(
        slug=slug,
        defaults={
            'category': category,
            'name': p_data['name'],
            'description': p_data['desc'],
            'price': p_data['price'],
            'stock': 20,
            'available': True,
            'featured': True if 'Pro' in p_data['name'] or 'Premium' in p_data['name'] else False
        }
    )
    
    if created or not product.image:
        image_data = generate_image_for_product(p_data['keywords'])
        if image_data:
            product.image.save(f"{slug}.jpg", ContentFile(image_data), save=True)
            print(f"Saved {product.name}")

def run():
    print("Clearing old products")
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    print("Creating Categories...")
    for cat_name in CATEGORIES.keys():
        Category.objects.create(name=cat_name, slug=slugify(cat_name))
        
    print("Creating Products and downloading images sequentially...")
    for cat_name, products in CATEGORIES.items():
        for p_data in products:
            process_product(cat_name, p_data)
                
    print("Database seeding completed successfully.")

if __name__ == '__main__':
    run()
