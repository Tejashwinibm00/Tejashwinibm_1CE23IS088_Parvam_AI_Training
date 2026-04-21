"""Download product images (from product.image URL) into local static/images
and update the Product.image to the local path (so templates use local images).

Run this from the project root using the venv python: 
.\.venv\Scripts\python.exe download_images.py
"""
import os
import requests
from app import app
from models import db, Product

OUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')
os.makedirs(OUT_DIR, exist_ok=True)

def make_image_url(term: str, pid: int) -> str:
    # Use picsum.photos seeded images so we get deterministic images without API keys.
    # Seed with product id and term to vary images.
    safe = term.replace(' ', '+')
    seed = f"{safe}-{pid}"
    return f"https://picsum.photos/seed/{seed}/600/400"

def download(url, path):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False
    with open(path, 'wb') as f:
        f.write(resp.content)
    return True

def main():
    with app.app_context():
        products = Product.query.all()
        print(f"Found {len(products)} products to process")
        for p in products:
            # determine source url: use picsum seeded by product id and name
            src = make_image_url(p.name or 'product', p.id)
            # create filename based on id
            fname = f"product_{p.id}.jpg"
            outpath = os.path.join(OUT_DIR, fname)
            if os.path.exists(outpath) and os.path.getsize(outpath) > 1024:
                # already downloaded
                p.image = f"images/{fname}"
                continue
            # retry a few times for robustness
            ok = False
            for attempt in range(3):
                if download(src, outpath):
                    ok = True
                    break
            if not ok:
                # fallback to picsum random to try to get any image
                fallback = f"https://picsum.photos/600/400?random={p.id}"
                ok = download(fallback, outpath)
            if ok:
                p.image = f"images/{fname}"
                print(f"Saved {p.id} -> {fname}")
            else:
                print(f"Using placeholder for product {p.id}")
        db.session.commit()
        print("Done. Updated product.image to local files under static/images/")

if __name__ == '__main__':
    main()
