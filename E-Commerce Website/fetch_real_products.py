"""
Fetch real product metadata and images from given product page URLs.

WARNING: Scraping commercial sites (Amazon, Flipkart, Meesho) may violate
their Terms of Service. Use this script only for learning/demos or when you
have permission. Prefer official APIs where available.

Usage:
  - Create a file `product_urls.csv` with columns: id,url
    where `id` is the target product id in your database you want to update.
  - Or create `urls.txt` with one URL per line; the script will try to match
    scraped product title to an existing product by substring.

Run:
  .\.venv\Scripts\python.exe fetch_real_products.py

Behavior:
  - For each URL, the script fetches the page, extracts `og:image` or the
    first large image, downloads it to `static/images/product_{id}.jpg`, and
    updates the corresponding `Product.image` to that local path. If a local
    image existed it is removed first.
"""
import csv
import os
import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from app import app
from models import db, Product

IMG_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')
os.makedirs(IMG_DIR, exist_ok=True)


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; ProductFetcher/1.0)'
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.text


def extract_image_and_title(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    # Open Graph image
    og_image = None
    og_title = None
    og = soup.find('meta', property='og:image')
    if og and og.get('content'):
        og_image = og['content']
    ogt = soup.find('meta', property='og:title')
    if ogt and ogt.get('content'):
        og_title = ogt['content']

    # fallback: link rel=image_src
    if not og_image:
        link_img = soup.find('link', rel='image_src')
        if link_img and link_img.get('href'):
            og_image = link_img['href']

    # fallback: find largest image by dimensions (heuristic)
    if not og_image:
        imgs = soup.find_all('img')
        candidates = []
        for img in imgs:
            src = img.get('src') or img.get('data-src') or img.get('data-original')
            if not src:
                continue
            # skip tiny icons
            width = img.get('width')
            height = img.get('height')
            try:
                w = int(width) if width else 0
                h = int(height) if height else 0
            except Exception:
                w = h = 0
            score = w * h
            candidates.append((score, src))
        if candidates:
            candidates.sort(reverse=True)
            og_image = candidates[0][1]

    # Sanitize URLs (relative -> absolute)
    if og_image and og_image.startswith('//'):
        parsed = urlparse(url)
        og_image = f"{parsed.scheme}:{og_image}"
    elif og_image and og_image.startswith('/'):
        parsed = urlparse(url)
        og_image = f"{parsed.scheme}://{parsed.netloc}{og_image}"

    # title fallback
    if not og_title:
        t = soup.find('title')
        if t:
            og_title = t.text.strip()

    return og_image, og_title


def download_image(url, outpath):
    try:
        resp = requests.get(url, stream=True, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        return False, str(e)
    with open(outpath, 'wb') as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
    return True, None


def run():
    # Read product_urls.csv if exists (id,url)
    csv_path = os.path.join(os.path.dirname(__file__), 'product_urls.csv')
    txt_path = os.path.join(os.path.dirname(__file__), 'urls.txt')

    pairs = []  # list of (maybe_id, url)
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                if len(row) >= 2 and row[0].strip().isdigit():
                    pairs.append((int(row[0].strip()), row[1].strip()))
                else:
                    pairs.append((None, row[0].strip()))
    elif os.path.exists(txt_path):
        with open(txt_path, encoding='utf-8') as f:
            for line in f:
                u = line.strip()
                if u:
                    pairs.append((None, u))
    else:
        print('Provide product_urls.csv (id,url) or urls.txt with URLs, then re-run.')
        return

    with app.app_context():
        for maybe_id, url in pairs:
            print('Processing', url)
            try:
                html = get_page(url)
            except Exception as e:
                print('  Failed to fetch page:', e)
                continue
            img_url, title = extract_image_and_title(html, url)
            print('  title=', title)
            print('  img=', img_url)

            target_id = maybe_id
            if target_id is None and title:
                # try to match by substring against product names
                candidate = Product.query.filter(Product.name.ilike(f"%{title[:40]}%"))
                first = candidate.first()
                if first:
                    target_id = first.id
                    print(f'  matched to product id {target_id} by title')

            if target_id is None:
                print('  No target id found; skipping (provide id in product_urls.csv to update DB)')
                continue

            p = Product.query.get(target_id)
            if not p:
                print(f'  Product id {target_id} not found in DB; skipping')
                continue

            # remove old local image if present
            if p.image and not p.image.startswith('http'):
                old_path = os.path.join(os.path.dirname(__file__), 'static', p.image.replace('/', os.sep))
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                        print('  removed old image', old_path)
                    except Exception as e:
                        print('  failed to remove old image:', e)

            if not img_url:
                print('  no image found on page; skipping')
                continue

            outname = f'product_{target_id}.jpg'
            outpath = os.path.join(IMG_DIR, outname)
            ok, err = download_image(img_url, outpath)
            if not ok:
                print('  failed to download image:', err)
                continue
            # update DB
            p.image = f'images/{outname}'
            db.session.commit()
            print(f'  updated product {target_id} image -> {p.image}')
            # be polite
            time.sleep(1)


if __name__ == '__main__':
    run()
