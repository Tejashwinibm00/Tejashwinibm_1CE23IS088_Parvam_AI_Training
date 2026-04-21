"""Seed script to create DB and a large set of sample categories/products.

This script creates three categories (Electronics, Beauty, Phones) and
populates the database with 60+ example products. Each product uses the
Unsplash Source API to provide a realistic image URL so the UI displays
real photographs (hotlinked).
"""
from app import app
from models import db, Category, Product, User
import random


def make_image_url(term: str) -> str:
    # Use Unsplash Source to get a relevant photo for the product term.
    safe = term.replace(' ', '+')
    return f"https://source.unsplash.com/600x400/?{safe}"


def seed():
    with app.app_context():
        db.create_all()

        # create categories if they don't exist
        electronics = Category.query.filter_by(name='Electronics').first()
        beauty = Category.query.filter_by(name='Beauty').first()
        phones = Category.query.filter_by(name='Phones').first()
        if not electronics:
            electronics = Category(name='Electronics', description='Electronic gadgets and accessories')
            db.session.add(electronics)
        if not beauty:
            beauty = Category(name='Beauty', description='Branded beauty and personal care')
            db.session.add(beauty)
        if not phones:
            phones = Category(name='Phones', description='Smartphones, cases, and accessories')
            db.session.add(phones)
        db.session.commit()

        existing = Product.query.count()
        per_category_target = 60  # create 60+ products per category

        products = []

        # Electronics base items
        electronics_items = [
            ('Smart TV', '4K HDR Smart television'),
            ('Bluetooth Headphones', 'Noise cancelling wireless headphones'),
            ('Wireless Mouse', 'Ergonomic mouse with fast scrolling'),
            ('Gaming Laptop', 'High performance laptop for gaming'),
            ('4K Monitor', 'Ultra HD monitor with vivid colors'),
            ('Smart Speaker', 'Voice assistant enabled speaker'),
            ('Portable SSD', 'Fast external solid state drive'),
            ('Fitness Tracker', 'Wearable activity and sleep tracker'),
            ('Action Camera', 'Waterproof action camera'),
            ('Drone', 'Camera drone with stabilization'),
        ]

        # Beauty items
        beauty_items = [
            ('Luxury Perfume', 'Signature scent from a top brand'),
            ('Lipstick', 'Long-lasting matte lipstick'),
            ('Moisturizer', 'Hydrating face cream'),
            ('Foundation', 'Liquid foundation with full coverage'),
            ('Shampoo', 'Sulfate-free shampoo for daily use'),
            ('Conditioner', 'Nourishing conditioner for smooth hair'),
            ('Face Serum', 'Anti-aging vitamin C serum'),
            ('Sunscreen', 'SPF 50 broad-spectrum sunscreen'),
        ]

        # Phones items
        phones_items = [
            ('Phone Model', 'Latest model smartphone'),
            ('Phone Case', 'Protective case for smartphones'),
            ('Screen Protector', 'Tempered glass protector'),
            ('Wireless Charger', 'Fast wireless charging pad'),
            ('Earbuds', 'True wireless earbuds with charging case'),
        ]

        # generate multiple variants for each base item
        for idx in range(1, per_category_target + 1):
            name, desc = electronics_items[(idx - 1) % len(electronics_items)]
            pname = f"{name} {idx}"
            price = round(random.uniform(19.99, 1299.99), 2)
            img = make_image_url(name)
            products.append(Product(name=pname, description=desc, price=price, image=img, category_id=electronics.id))

        for idx in range(1, per_category_target + 1):
            name, desc = beauty_items[(idx - 1) % len(beauty_items)]
            pname = f"{name} {idx}"
            price = round(random.uniform(5.99, 199.99), 2)
            img = make_image_url(name)
            products.append(Product(name=pname, description=desc, price=price, image=img, category_id=beauty.id))

        for idx in range(1, per_category_target + 1):
            name, desc = phones_items[(idx - 1) % len(phones_items)]
            pname = f"{name} {idx}"
            price = round(random.uniform(9.99, 999.99), 2)
            img = make_image_url(name)
            products.append(Product(name=pname, description=desc, price=price, image=img, category_id=phones.id))

        # add generated products
        db.session.add_all(products)

        # create admin user if none
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(email='admin@example.com', password_hash='pbkdf2:sha256:100000$dev$hash', is_admin=True)
            db.session.add(admin)

        db.session.commit()
        print(f"Seeded database with {len(products)} products.")


if __name__ == '__main__':
    seed()
