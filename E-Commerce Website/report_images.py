"""Generate a report of product images and optionally remove images that don't match product names.

Usage:
  .\.venv\Scripts\python.exe report_images.py    # writes report.csv
  .\.venv\Scripts\python.exe report_images.py --clean   # also remove local images for products with no keyword
"""
import csv
import os
import argparse
import re
from app import app
from models import Product, db

KEYWORD_MAP = {
    'tv': 'television', 'smart tv': 'television', 'headphone': 'headphones', 'headphones': 'headphones',
    'mouse': 'computer-mouse', 'laptop': 'laptop', 'gaming': 'gaming', 'monitor': 'monitor',
    'speaker': 'speaker', 'ssd': 'ssd', 'fitness': 'fitness-tracker', 'tracker': 'fitness-tracker',
    'camera': 'camera', 'drone': 'drone', 'perfume': 'perfume', 'lipstick': 'lipstick',
    'moisturizer': 'skincare', 'foundation': 'makeup', 'shampoo': 'shampoo', 'conditioner': 'conditioner',
    'serum': 'serum', 'sunscreen': 'sunscreen', 'phone': 'smartphone', 'case': 'phone-case',
    'screen': 'screen-protector', 'charger': 'charger', 'earbuds': 'earbuds', 'earbud': 'earbuds',
}

def find_keyword(name: str):
    n = (name or '').lower()
    for k in sorted(KEYWORD_MAP.keys(), key=lambda x: -len(x)):
        if k in n:
            return KEYWORD_MAP[k]
    return None


def main(clean=False):
    report_path = os.path.join(os.path.dirname(__file__), 'report.csv')
    rows = []
    with app.app_context():
        products = Product.query.order_by(Product.id).all()
        for p in products:
            keyword = find_keyword(p.name)
            image = p.image or ''
            local_path = ''
            if image and not image.startswith('http'):
                local_path = os.path.join(os.path.dirname(__file__), 'static', image.replace('/', os.sep))
            rows.append({'id': p.id, 'name': p.name, 'image': image, 'keyword': keyword, 'local_path': local_path})

    # write CSV
    with open(report_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id','name','image','keyword','local_path'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Wrote report to {report_path} ({len(rows)} products)")

    if clean:
        removed = 0
        for r in rows:
            if not r['keyword'] and r['local_path'] and os.path.exists(r['local_path']):
                try:
                    os.remove(r['local_path'])
                    removed += 1
                    print(f"Removed image for product {r['id']}: {r['local_path']}")
                except Exception as e:
                    print(f"Failed to remove {r['local_path']}: {e}")
        print(f"Removed {removed} images for products without keyword.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean', action='store_true', help='Remove local images for products with no keyword match')
    args = parser.parse_args()
    main(clean=args.clean)
