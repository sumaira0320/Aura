import os
import django
import urllib.request
from django.core.files.base import ContentFile
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Category, Product

# Dictionary mapping exact book names to their precise ISBNs for fetching covers
BOOKS = {
    'Python Crash Course': '9781593279288',
    'The Great Gatsby': '9780743273565',
    'Clean Code': '9780132350884',
    'Atomic Habits': '9780735211292',
    'The Pragmatic Programmer': '9780135957059',
    'Designing Data-Intensive Applications': '9781449373320',
    'Dune': '9780441172719',
    'Sapiens: A Brief History of Humankind': '9780062316097',
    'Deep Work': '9781455586691'
}

def fix_books():
    print("Fixing book covers...")
    for book_name, isbn in BOOKS.items():
        try:
            product = Product.objects.get(name=book_name)
            url = f"http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
            
            print(f"Fetching {book_name} cover from {url}...")
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=10)
            image_data = resp.read()
            
            # OpenLibrary API returns a 1x1 transparent GIF if the cover is missing. 
            # Check file size to ensure it's a real image (usually > 1KB).
            if len(image_data) < 1000:
                print(f"Warning: Cover for {book_name} might be missing in OpenLibrary (size: {len(image_data)} bytes).")
                # Fallback to alternative OpenLibrary ID if needed, but let's assume valid for now
                if book_name == 'Python Crash Course': url = "http://covers.openlibrary.org/b/isbn/9781593276034-L.jpg"
                if book_name == 'Dune': url = "http://covers.openlibrary.org/b/isbn/9780441172719-L.jpg"
                resp = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
                image_data = resp.read()
            
            slug = slugify(book_name)
            
            # Delete old image file to save space
            if product.image:
                old_path = product.image.path
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            product.image.save(f"{slug}-cover.jpg", ContentFile(image_data), save=True)
            print(f"Successfully updated image for {book_name}")
            
        except Product.DoesNotExist:
            print(f"Error: Book '{book_name}' not found in database.")
        except Exception as e:
            print(f"Error updating {book_name}: {e}")

if __name__ == '__main__':
    fix_books()
