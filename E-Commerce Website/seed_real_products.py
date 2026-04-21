from app import app
from models import db, Category, Product, User
import random

def seed():
    with app.app_context():
        # Clear existing products and categories to start fresh
        db.drop_all()
        db.create_all()

        # Create categories
        electronics = Category(name='Electronics', description='Latest gadgets, laptops, and tech accessories.')
        beauty = Category(name='Beauty', description='Premium skincare, makeup, and personal care products.')
        phones = Category(name='Phones', description='Top-tier smartphones and mobile accessories.')
        
        db.session.add_all([electronics, beauty, phones])
        db.session.commit()

        # Electronics (30+ products)
        electronics_products = [
            ("Sony WH-1000XM5", "Industry-leading noise canceling wireless headphones.", 399.99),
            ("Apple MacBook Pro M3", "14-inch laptop with the powerful M3 chip.", 1599.00),
            ("Samsung Galaxy Tab S9", "11-inch AMOLED display with S Pen included.", 799.99),
            ("Logitech MX Master 3S", "Performance wireless mouse with ultra-fast scrolling.", 99.00),
            ("Dell XPS 15", "Powerful laptop with stunning InfinityEdge display.", 1899.00),
            ("Bose QuietComfort Ultra", "Premium noise cancelling earbuds with spatial audio.", 299.00),
            ("Nintendo Switch OLED", "Handheld gaming console with a vibrant OLED screen.", 349.99),
            ("PlayStation 5 Slim", "The latest version of the popular gaming console.", 499.99),
            ("Xbox Series X", "The fastest, most powerful Xbox ever.", 499.00),
            ("GoPro Hero 12 Black", "Ultimate action camera with 5.3K video.", 399.00),
            ("DJI Mini 4 Pro", "Ultralight folding drone with 4K HDR video.", 759.00),
            ("Apple Watch Series 9", "Advanced health sensors and powerful performance.", 399.00),
            ("Garmin Fenix 7", "Multisport GPS watch with solar charging.", 649.99),
            ("Kindle Paperwhite", "Waterproof e-reader with a 6.8\" display.", 139.99),
            ("Sonos Era 100", "Compact smart speaker with room-filling sound.", 249.00),
            ("Razer DeathAdder V3", "Pro-grade wired gaming mouse for esports.", 69.99),
            ("ASUS ROG Zephyrus G14", "Compact and powerful gaming laptop.", 1499.00),
            ("HP Spectre x360", "Premium 2-in-1 laptop with 4K touch display.", 1299.00),
            ("Microsoft Surface Pro 9", "Powerful tablet-to-laptop versatility.", 999.00),
            ("Canon EOS R6 Mark II", "Full-frame mirrorless camera for pros.", 2499.00),
            ("Fujifilm X-T5", "Mirrorless camera with classic design.", 1699.00),
            ("Sony Alpha a7 IV", "The versatile hybrid mirrorless camera.", 2499.99),
            ("LG C3 OLED TV", "Stunning 4K OLED TV for gaming and movies.", 1299.00),
            ("Samsung Odyssey Neo G9", "57-inch dual UHD curved gaming monitor.", 2499.00),
            ("Corsair K70 RGB TKL", "Optical-mechanical gaming keyboard.", 139.99),
            ("SteelSeries Arctis Nova Pro", "High-fidelity gaming headset.", 349.99),
            ("Razer Naga V2 Pro", "Wireless MMO gaming mouse with interchangeable side plates.", 179.99),
            ("Logitech G Pro X 2 Lightspeed", "Wireless gaming headset with graphene drivers.", 249.00),
            ("SteelSeries Apex Pro TKL", "World's fastest adjustable mechanical keyboard.", 189.99),
            ("Elgato Facecam Pro", "The first 4K60 webcam with professional-grade optics.", 299.99),
            ("HyperX QuadCast S", "RGB USB condenser microphone for streamers.", 159.99),
            ("Blue Compass Boom Arm", "Premium broadcast boom arm with internal springs.", 99.00)
        ]

        # Beauty (30+ products)
        beauty_products = [
            ("Estée Lauder Night Repair", "Advanced recovery serum for all skin types.", 115.00),
            ("Clinique Moisture Surge", "Hydrating gel-cream for 100 hours of moisture.", 44.00),
            ("Lancôme Génifique", "Anti-aging serum for radiant skin.", 88.00),
            ("La Mer Crème de la Mer", "Luxurious moisturizing cream.", 190.00),
            ("The Ordinary Niacinamide", "Vitamin B3 serum to reduce blemishes.", 6.00),
            ("CeraVe Facial Cleanser", "Hydrating cleanser for normal to dry skin.", 15.99),
            ("Paula's Choice 2% BHA", "Exfoliant for smooth and clear skin.", 34.00),
            ("Drunk Elephant Lala Retro", "Whipped cream for skin barrier support.", 60.00),
            ("Sunday Riley Good Genes", "Lactic acid treatment for instant glow.", 85.00),
            ("Glossier Boy Brow", "Fluffy, groomed brows in a swipe.", 18.00),
            ("Fenty Beauty Foundation", "Full coverage foundation in 50 shades.", 39.00),
            ("NARS Creamy Concealer", "Luminous concealer for flawless skin.", 32.00),
            ("Charlotte Tilbury Cream", "Instant turnaround moisturizer.", 100.00),
            ("Laneige Lip Mask", "Soothing lip sleeping mask.", 24.00),
            ("Tatcha The Water Cream", "Oil-free moisturizer for clear skin.", 70.00),
            ("Kiehl's Ultra Facial Cream", "Classic 24-hour daily moisturizer.", 38.00),
            ("SK-II Treatment Essence", "Miracle water for crystal clear skin.", 199.00),
            ("Shiseido Ultimune", "Power infusing concentrate for immunity.", 75.00),
            ("Dior Sauvage", "Classic men's fragrance.", 115.00),
            ("Chanel No. 5", "Timeless floral fragrance.", 135.00),
            ("Olaplex No. 3", "Hair repair treatment for all types.", 30.00),
            ("Dyson Airwrap", "Multi-styler for all hair types.", 599.00),
            ("Revlon One-Step", "Volumizer hair dryer and hot air brush.", 39.99),
            ("Moroccanoil Treatment", "Argan oil hair treatment.", 48.00),
            ("Living Proof Dry Shampoo", "Clean hair without the wash.", 28.00),
            ("Briogeo Hair Mask", "Deep conditioning hair mask.", 39.00),
            ("Olaplex No. 4 Shampoo", "Bond maintenance shampoo for hair repair.", 30.00),
            ("Olaplex No. 5 Conditioner", "Bond maintenance conditioner for hydration.", 30.00),
            ("Kérastase Elixir Ultime", "L'Original hair oil for shine and protection.", 54.00),
            ("Dyson Supersonic", "High-speed hair dryer with intelligent heat control.", 429.00),
            ("YSL Libre Eau de Parfum", "The fragrance of freedom with lavender and orange blossom.", 130.00),
            ("Sol de Janeiro Bum Bum Cream", "Fast-absorbing body cream with a pistachio-caramel scent.", 48.00)
        ]

        # Phones (30+ products)
        phones_products = [
            ("iPhone 15 Pro Max", "The ultimate iPhone with titanium design.", 1199.00),
            ("Samsung Galaxy S24 Ultra", "Power and precision with Galaxy AI.", 1299.00),
            ("Google Pixel 8 Pro", "The best of Google AI in your pocket.", 999.00),
            ("OnePlus 12", "Smooth and fast flagship performance.", 799.00),
            ("iPhone 15", "Dynamic Island and advanced dual-camera.", 799.00),
            ("Samsung Galaxy S24", "AI-powered compact flagship.", 799.00),
            ("Google Pixel 8", "Powerful AI and amazing camera.", 699.00),
            ("iPhone 14", "Proven performance and battery life.", 699.00),
            ("Samsung Galaxy A54", "Awesome 5G performance at a great value.", 449.00),
            ("Google Pixel 7a", "The essential Pixel features for less.", 499.00),
            ("Motorola Edge 40 Pro", "Fast performance and rapid charging.", 899.00),
            ("Xiaomi 14 Ultra", "Professional-grade photography smartphone.", 1299.00),
            ("Asus Zenfone 10", "Compact power in a pocket-friendly size.", 699.00),
            ("Nothing Phone (2)", "Unique Glyph Interface and sleek design.", 599.00),
            ("Sony Xperia 1 V", "Alpha-tech camera in a smartphone.", 1399.00),
            ("Samsung Galaxy Z Fold 5", "The ultimate multitasking foldable.", 1799.00),
            ("Samsung Galaxy Z Flip 5", "Compact and stylish foldable phone.", 999.00),
            ("iPhone 15 Plus", "Large display and incredible battery.", 899.00),
            ("iPhone 15 Pro", "A17 Pro chip and pro camera system.", 999.00),
            ("Google Pixel Fold", "Google's first foldable smartphone.", 1799.00),
            ("Motorola Razr Plus", "Iconic flip design with modern tech.", 999.00),
            ("Huawei P60 Pro", "Ultra-lighting photography flagship.", 1199.00),
            ("Oppo Find X6 Pro", "Hasselblad camera system flagship.", 1099.00),
            ("Vivo X100 Pro", "Zeiss optics for stunning photography.", 999.00),
            ("Honor Magic 6 Pro", "Next-gen eye-tracking technology.", 1199.00),
            ("RealMe GT 5", "Ultra-fast charging and performance.", 499.00),
            ("iPhone 13", "Advanced dual-camera system and A15 Bionic.", 599.00),
            ("Samsung Galaxy S23", "Performance and quality you can trust.", 699.00),
            ("Google Pixel 7", "The all-pro Google phone at a great price.", 599.00),
            ("Motorola Razr 40 Ultra", "The largest external display on a flip phone.", 899.00),
            ("Asus ROG Phone 8 Pro", "The ultimate gaming smartphone.", 1199.00),
            ("Xiaomi 13 Pro", "Co-engineered with Leica for legendary photos.", 999.00)
        ]


        def get_img(name):
            # Fallback to unsplash for now, we'll try to find real ones later
            safe = name.replace(' ', '+')
            return f"https://source.unsplash.com/600x400/?{safe}"

        products = []
        for name, desc, price in electronics_products:
            products.append(Product(name=name, description=desc, price=price, image=get_img(name), category_id=electronics.id))
        
        for name, desc, price in beauty_products:
            products.append(Product(name=name, description=desc, price=price, image=get_img(name), category_id=beauty.id))
            
        for name, desc, price in phones_products:
            products.append(Product(name=name, description=desc, price=price, image=get_img(name), category_id=phones.id))

        db.session.add_all(products)

        # Create admin user
        admin = User(email='admin@example.com', password_hash='pbkdf2:sha256:100000$dev$hash', is_admin=True)
        db.session.add(admin)

        db.session.commit()
        print(f"Seeded database with {len(products)} real products.")

if __name__ == '__main__':
    seed()
