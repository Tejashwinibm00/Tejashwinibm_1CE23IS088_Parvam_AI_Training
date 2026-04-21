const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./db.sqlite');

// Create products table if not exists
db.run(`CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  description TEXT,
  price REAL,
  stock INTEGER,
  category TEXT,
  image_url TEXT
)`);

// Insert one sample product
db.run("INSERT INTO products (name, description, price, stock, category, image_url) VALUES (?, ?, ?, ?, ?, ?)",
  ["Sample Product", "This is a test product", 100, 10, "electronics", "https://via.placeholder.com/150"]);

console.log("Seed complete!");

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./db.sqlite');

db.run(`CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  description TEXT,
  price REAL,
  stock INTEGER,
  category TEXT,
  image_url TEXT
)`);


db.run("INSERT INTO products(name, description, price, stock, category, image_url) VALUES(?, ?, ?, ?, ?, ?)",
  ["Sample Product", "This is a test product", 100, 10, "electronics", "https://via.placeholder.com/150"]);

console.log("Seed complete!");
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./db.sqlite');

const categories = {
  electronics: [
    { name: "Laptop Pro 15", description: "High performance laptop", price: 1200, stock: 20, image_url: "https://via.placeholder.com/150" },
    { name: "Smart TV 55\"", description: "4K Ultra HD Smart TV", price: 800, stock: 15, image_url: "https://via.placeholder.com/150" },
    { name: "Bluetooth Headphones", description: "Noise cancelling wireless headphones", price: 150, stock: 50, image_url: "https://via.placeholder.com/150" },
    { name: "Gaming Console X", description: "Next-gen gaming console", price: 500, stock: 25, image_url: "https://via.placeholder.com/150" },
    { name: "Smartwatch Z", description: "Fitness tracking smartwatch", price: 200, stock: 40, image_url: "https://via.placeholder.com/150" },
    { name: "Wireless Mouse", description: "Ergonomic wireless mouse", price: 30, stock: 100, image_url: "https://via.placeholder.com/150" },
    { name: "Mechanical Keyboard", description: "RGB backlit keyboard", price: 90, stock: 60, image_url: "https://via.placeholder.com/150" },
    { name: "External SSD 1TB", description: "Portable solid state drive", price: 120, stock: 70, image_url: "https://via.placeholder.com/150" },
    { name: "Drone Camera", description: "HD camera drone", price: 350, stock: 15, image_url: "https://via.placeholder.com/150" },
    { name: "Home Theater System", description: "Surround sound system", price: 600, stock: 10, image_url: "https://via.placeholder.com/150" },
    // … add 20 more electronics items
  ],
  beauty: [
    { name: "Luxury Lipstick", description: "Branded matte lipstick", price: 25, stock: 100, image_url: "https://via.placeholder.com/150" },
    { name: "Perfume Classic", description: "Premium fragrance", price: 60, stock: 50, image_url: "https://via.placeholder.com/150" },
    { name: "Moisturizing Cream", description: "Hydrating skin cream", price: 40, stock: 80, image_url: "https://via.placeholder.com/150" },
    { name: "Shampoo Herbal", description: "Organic hair shampoo", price: 15, stock: 120, image_url: "https://via.placeholder.com/150" },
    { name: "Face Wash Gentle", description: "Daily cleansing face wash", price: 12, stock: 150, image_url: "https://via.placeholder.com/150" },
    { name: "Nail Polish Set", description: "Pack of 5 colors", price: 20, stock: 90, image_url: "https://via.placeholder.com/150" },
    { name: "Sunscreen SPF50", description: "UV protection sunscreen", price: 18, stock: 110, image_url: "https://via.placeholder.com/150" },
    { name: "Hair Dryer Pro", description: "Salon quality hair dryer", price: 70, stock: 30, image_url: "https://via.placeholder.com/150" },
    { name: "Eye Shadow Palette", description: "12 color palette", price: 35, stock: 60, image_url: "https://via.placeholder.com/150" },
    { name: "Luxury Serum", description: "Anti-aging serum", price: 90, stock: 40, image_url: "https://via.placeholder.com/150" },
    // … add 20 more beauty items
  ],
  phones: [
    { name: "Phone X", description: "Latest flagship smartphone", price: 999, stock: 30, image_url: "https://via.placeholder.com/150" },
    { name: "Budget Phone Y", description: "Affordable smartphone", price: 299, stock: 40, image_url: "https://via.placeholder.com/150" },
    { name: "Phone Z Ultra", description: "Large screen smartphone", price: 799, stock: 25, image_url: "https://via.placeholder.com/150" },
    { name: "Foldable Phone A", description: "Innovative foldable design", price: 1200, stock: 15, image_url: "https://via.placeholder.com/150" },
    { name: "Gaming Phone B", description: "High refresh rate display", price: 650, stock: 20, image_url: "https://via.placeholder.com/150" },
    { name: "Phone C Lite", description: "Compact smartphone", price: 450, stock: 35, image_url: "https://via.placeholder.com/150" },
    { name: "Phone D Max", description: "High battery capacity", price: 550, stock: 40, image_url: "https://via.placeholder.com/150" },
    { name: "Phone E 5G", description: "Fast 5G connectivity", price: 700, stock: 30, image_url: "https://via.placeholder.com/150" },
    { name: "Phone F Mini", description: "Small and lightweight", price: 250, stock: 50, image_url: "https://via.placeholder.com/150" },
    { name: "Phone G Pro", description: "Professional camera system", price: 1100, stock: 20, image_url: "https://via.placeholder.com/150" },
    // … add 20 more phone items
  ]
};

for (let category in categories) {
  categories[category].forEach(p => {
    db.run("INSERT INTO products(name, description, price, stock, category, image_url) VALUES(?, ?, ?, ?, ?, ?)",
      [p.name, p.description, p.price, p.stock, category, p.image_url]);
  });
}

console.log("Seed complete!");
