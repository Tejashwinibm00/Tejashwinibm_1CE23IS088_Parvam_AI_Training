from app import app
from models import db, Product

def update_images():
    with app.app_context():
        # Map of product name keywords to real image URLs
        image_map = {
            "Sony WH-1000XM5": "https://m.media-amazon.com/images/I/61+9m6S0VLL._AC_SL1500_.jpg",
            "Apple MacBook Pro M3": "https://m.media-amazon.com/images/I/618S8uH56SL._AC_SL1500_.jpg",
            "Samsung Galaxy Tab S9": "https://m.media-amazon.com/images/I/71Y8v-Nf-UL._AC_SL1500_.jpg",
            "Logitech MX Master 3S": "https://m.media-amazon.com/images/I/614w3LuZTYL._AC_SL1500_.jpg",
            "iPhone 15 Pro Max": "https://m.media-amazon.com/images/I/81Os1ndA5DL._AC_SL1500_.jpg",
            "Samsung Galaxy S24 Ultra": "https://m.media-amazon.com/images/I/71WjsZqiPxL._AC_SL1500_.jpg",
            "OnePlus 12": "https://m.media-amazon.com/images/I/71-L6X7-A2L._AC_SL1500_.jpg",
            "Google Pixel 8 Pro": "https://m.media-amazon.com/images/I/71W8S7tZInL._AC_SL1500_.jpg",
            "Nintendo Switch OLED": "https://m.media-amazon.com/images/I/816nS+2q7IL._AC_SL1500_.jpg",
            "PlayStation 5": "https://m.media-amazon.com/images/I/51051HiS9OL._AC_SL1200_.jpg",
            "Xbox Series X": "https://m.media-amazon.com/images/I/61JG6loX80L._AC_SL1500_.jpg",
            "Estée Lauder": "https://m.media-amazon.com/images/I/61P9vP6XWkL._AC_SL1500_.jpg",
            "Clinique": "https://m.media-amazon.com/images/I/51Xm8mZ+M1L._AC_SL1000_.jpg",
            "Dyson Airwrap": "https://m.media-amazon.com/images/I/61YF+eY4-EL._AC_SL1500_.jpg",
            "Fenty Beauty": "https://m.media-amazon.com/images/I/51eS9uN8tSL._AC_SL1000_.jpg",
        }

        products = Product.query.all()
        count = 0
        for p in products:
            for key, url in image_map.items():
                if key.lower() in p.name.lower():
                    p.image = url
                    count += 1
                    break
            
            # For others, use a high-quality Unsplash search that includes the product name
            if not p.image.startswith('http'):
                safe_name = p.name.replace(' ', '+')
                p.image = f"https://source.unsplash.com/featured/600x400?{safe_name},product"

        db.session.commit()
        print(f"Updated {count} products with specific real images and {len(products)-count} with themed Unsplash images.")

if __name__ == '__main__':
    update_images()
