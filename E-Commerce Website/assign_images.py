"""Assign more relevant images to products based on keywords in their names.

This script uses picsum.photos seeded images for themed photos. For each
product it looks for known keywords and assigns an image seeded with that
keyword. If no suitable keyword is found the product.image is cleared to the
SVG placeholder and any previously downloaded local file is removed.

Run with the project's venv python:
.\.venv\Scripts\python.exe assign_images.py
"""
import os
import re
import requests
from app import app
from models import db, Product

OUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')
PLACEHOLDER = 'placeholder.svg'

# keyword -> picsum seed term
KEYWORD_MAP = {
    'tv': 'television',
    'smart tv': 'television',
    'headphone': 'headphones',
    'headphones': 'headphones',
    'mouse': 'computer-mouse',
    'laptop': 'laptop',
    'gaming': 'gaming',
    'monitor': 'monitor',
    'speaker': 'speaker',
    'ssd': 'ssd',
    'fitness': 'fitness-tracker',
    'tracker': 'fitness-tracker',
    'camera': 'camera',
    'drone': 'drone',
    'perfume': 'perfume',
    'lipstick': 'lipstick',
    'moisturizer': 'skincare',
    'foundation': 'makeup',
    'shampoo': 'shampoo',
    'conditioner': 'conditioner',
    'serum': 'serum',
    'sunscreen': 'sunscreen',
    'phone': 'smartphone',
    'case': 'phone-case',
    'screen': 'screen-protector',
    'charger': 'charger',
    'earbuds': 'earbuds',
    'earbud': 'earbuds',
}


def themed_url(seed_term: str, pid: int) -> str:
    safe = re.sub(r"\s+", '-', seed_term)
    seed = f"{safe}-{pid}"
    return f"https://picsum.photos/seed/{seed}/600/400"


def download(url, path):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        return False, str(e)
    with open(path, 'wb') as f:
        f.write(resp.content)
    return True, None


def find_keyword(name: str):
    n = name.lower()
    for k in sorted(KEYWORD_MAP.keys(), key=lambda x: -len(x)):
        if k in n:
            return KEYWORD_MAP[k]
    return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    updated = 0
    cleared = 0
    with app.app_context():
        products = Product.query.all()
        for p in products:
            keyword = find_keyword(p.name or '')
            fname = f"product_{p.id}.jpg"
            outpath = os.path.join(OUT_DIR, fname)
            if keyword:
                url = themed_url(keyword, p.id)
                ok, err = download(url, outpath)
                if ok:
                    p.image = f"images/{fname}"
                    updated += 1
                else:
                    # leave existing image if download failed
                    print(f"Failed to download themed image for {p.id} ({p.name}): {err}")
            else:
                # clear product image and remove local file if present
                if os.path.exists(outpath):
                    try:
                        os.remove(outpath)
                    except Exception:
                        pass
                p.image = ''
                cleared += 1
        db.session.commit()

    print(f"Assigned themed images to {updated} products; cleared images for {cleared} products.")


if __name__ == '__main__':
    main()
