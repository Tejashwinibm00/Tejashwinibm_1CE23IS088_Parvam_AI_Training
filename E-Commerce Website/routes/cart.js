const express = require('express');
module.exports = (db) => {
  const router = express.Router();

  router.post('/add/:id', (req, res) => {
    const id = req.params.id;
    if (!req.session.cart) req.session.cart = {};
    req.session.cart[id] = (req.session.cart[id] || 0) + 1;
    res.redirect('/cart');
  });

  router.get('/', (req, res) => {
    res.render('cart/cart', { cart: req.session.cart || {} });
  });

  return router;
};
