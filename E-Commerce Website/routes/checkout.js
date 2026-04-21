const express = require('express');
module.exports = (db) => {
  const router = express.Router();

  router.get('/shipping', (req, res) => res.render('checkout/shipping'));
  router.post('/payment', (req, res) => res.render('checkout/payment'));
  router.post('/confirm', (req, res) => {
    const cart = req.session.cart || {};
    let total = 0;
    for (let id in cart) total += cart[id] * 10; // dummy calc

    db.run("INSERT INTO orders(user_id, total, status) VALUES(?, ?, ?)",
      [req.session.user?.id || 1, total, "paid"], function(err) {
        req.session.cart = {};
        res.render('checkout/confirmation', { orderId: this.lastID, total });
      });
  });

  return router;
};
