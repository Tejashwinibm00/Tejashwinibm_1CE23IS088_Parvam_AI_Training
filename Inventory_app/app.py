from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os
import csv
from io import StringIO
from datetime import datetime

app = Flask(__name__)

INVENTORY_FILE = "inventory.json"

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return {"products": []}
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

def save_inventory(data):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_product_status(products):
    """Update status based on stock level"""
    for product in products:
        if product["qty"] < product["min_threshold"]:
            product["status"] = "Low Stock"
        else:
            product["status"] = "In Stock"
    return products

@app.route("/")
def dashboard():
    inventory = load_inventory()
    products = inventory.get("products", [])
    products = update_product_status(products)

    low_stock_count = sum(1 for p in products if p["status"] == "Low Stock")
    categories = sorted(set(p["category"] for p in products if p.get("category")))

    return render_template("dashboard.html", products=products, low_stock_count=low_stock_count, categories=categories)

@app.route("/add", methods=["POST"])
def add_product():
    data = request.get_json()
    inventory = load_inventory()

    # Get next ID
    next_id = max([p["id"] for p in inventory["products"]], default=0) + 1

    new_product = {
        "id": next_id,
        "name": data.get("name"),
        "category": data.get("category"),
        "qty": int(data.get("qty", 0)),
        "min_threshold": int(data.get("min_threshold", 0)),
        "status": "Low Stock" if int(data.get("qty", 0)) < int(data.get("min_threshold", 0)) else "In Stock"
    }

    inventory["products"].append(new_product)
    save_inventory(inventory)

    return jsonify({"success": True, "product": new_product}), 201

@app.route("/edit/<int:product_id>", methods=["POST"])
def edit_product(product_id):
    data = request.get_json()
    inventory = load_inventory()

    for product in inventory["products"]:
        if product["id"] == product_id:
            product["name"] = data.get("name", product["name"])
            product["category"] = data.get("category", product["category"])
            product["qty"] = int(data.get("qty", product["qty"]))
            product["min_threshold"] = int(data.get("min_threshold", product["min_threshold"]))
            product["status"] = "Low Stock" if product["qty"] < product["min_threshold"] else "In Stock"
            break

    save_inventory(inventory)
    return jsonify({"success": True})

@app.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    inventory = load_inventory()
    inventory["products"] = [p for p in inventory["products"] if p["id"] != product_id]
    save_inventory(inventory)
    return jsonify({"success": True})

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    category = request.args.get("category", "")

    inventory = load_inventory()
    products = inventory.get("products", [])
    products = update_product_status(products)

    # Filter by search query
    if query:
        products = [p for p in products if query in p["name"].lower() or query in p["category"].lower()]

    # Filter by category
    if category:
        products = [p for p in products if p["category"] == category]

    low_stock_count = sum(1 for p in products if p["status"] == "Low Stock")
    categories = sorted(set(p["category"] for p in inventory["products"] if p.get("category")))

    return render_template("dashboard.html",
                         products=products,
                         low_stock_count=low_stock_count,
                         categories=categories,
                         search_query=query,
                         selected_category=category)

@app.route("/export-csv")
def export_csv():
    inventory = load_inventory()
    products = inventory.get("products", [])
    products = update_product_status(products)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Product Name", "Category", "Quantity", "Min Threshold", "Status"])

    for product in products:
        writer.writerow([
            product["id"],
            product["name"],
            product["category"],
            product["qty"],
            product["min_threshold"],
            product["status"]
        ])

    csv_content = output.getvalue()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"inventory_{timestamp}.csv"

    return csv_content, 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": f"attachment; filename={filename}"
    }

@app.route("/api/restock-suggestions")
def restock_suggestions():
    inventory = load_inventory()
    products = inventory.get("products", [])

    suggestions = []
    for product in products:
        if product["qty"] < product["min_threshold"]:
            deficit = product["min_threshold"] - product["qty"]
            suggestions.append({
                "id": product["id"],
                "name": product["name"],
                "current_qty": product["qty"],
                "min_threshold": product["min_threshold"],
                "restock_amount": deficit,
                "suggested_restock": deficit * 2  # Suggest restocking 2x the deficit
            })

    return jsonify({"suggestions": suggestions})

@app.route("/api/inventory")
def api_inventory():
    inventory = load_inventory()
    products = inventory.get("products", [])
    products = update_product_status(products)
    return jsonify({"products": products})

@app.route("/api/stats")
def stats():
    inventory = load_inventory()
    products = inventory.get("products", [])
    products = update_product_status(products)

    low_stock_count = sum(1 for p in products if p["status"] == "Low Stock")
    in_stock_count = sum(1 for p in products if p["status"] == "In Stock")
    total_products = len(products)

    return jsonify({
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "in_stock_count": in_stock_count
    })

if __name__ == "__main__":
    app.run(debug=True)