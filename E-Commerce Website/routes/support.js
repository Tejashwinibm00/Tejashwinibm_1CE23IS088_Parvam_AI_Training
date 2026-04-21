const express = require('express');
module.exports = () => {
  const router = express.Router();

  router.get('/contact', (req, res) => res.render('support/contact'));
  router.get('/shipping-info', (req, res) => res.render('support/shipping-info'));
  router.get('/store-locator', (req, res) => res.render('support/store-locator'));
  router.get('/signup', (req, res) => res.render('support/signup'));

  return router;
};
