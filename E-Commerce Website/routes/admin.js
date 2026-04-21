const express = require('express');
module.exports = (db) => {
  const router = express.Router();

  router.get('/dashboard', (req, res) => res.render('admin/dashboard'));
  router.get('/products', (req, res) => {
    db.all("SELECT * FROM products", [], (err, products) => {
      res.render('admin/products', { products });
    });
  });
  router.post('/products/add', (req, res) => {
    const { name, description, price, stock, category } = req.body;
    db.run("INSERT INTO products(name, description, price, stock, category) VALUES(?, ?, ?, ?, ?)",
      [name, description, price, stock, category], () => res.redirect('/admin/products'));
  });
  router.get('/orders', (req, res) => {
    db.all("SELECT * FROM orders", [], (err, orders) => {
      res.render('admin/orders', { orders });
    });
  });

  return router;
};
