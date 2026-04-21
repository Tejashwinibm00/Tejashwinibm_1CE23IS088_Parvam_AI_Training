const express = require('express');
module.exports = (db) => {
  const router = express.Router();

  router.get('/', (req, res) => {
    db.all("SELECT * FROM products LIMIT 12", [], (err, products) => {
      res.render('products/index', { products });
    });
  });

  router.get('/category/:name', (req, res) => {
    db.all("SELECT * FROM products WHERE category = ?", [req.params.name], (err, products) => {
      res.render('products/category', { products, category: req.params.name });
    });
  });

  router.get('/product/:id', (req, res) => {
    db.get("SELECT * FROM products WHERE id = ?", [req.params.id], (err, product) => {
      res.render('products/product', { product });
    });
  });

  router.get('/search', (req, res) => {
    const q = `%${req.query.q}%`;
    db.all("SELECT * FROM products WHERE name LIKE ?", [q], (err, products) => {
      res.render('products/search', { products, query: req.query.q });
    });
  });

  return router;
};
