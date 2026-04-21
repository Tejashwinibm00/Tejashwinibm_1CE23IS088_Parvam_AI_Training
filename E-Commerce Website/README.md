# Mini E-Commerce Website (MiniStore)

This is a small Flask-based e-commerce demo with product listing, session cart, checkout (dummy), and a minimal admin panel.

Setup (Windows PowerShell):

1. Create and activate venv

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Seed DB

```powershell
python seed.py
```

3. Run app

```powershell
python app.py
```

Default admin: admin@example.com (password not set — register and toggle is_admin in DB for quick access)
