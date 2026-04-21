const express = require('express');
module.exports = (db) => {
  const router = express.Router();

  router.get('/login', (req, res) => res.render('auth/login'));
  router.post('/login', (req, res) => {
    // Simplified login
    req.session.user = { id: 1, username: req.body.username };
    res.redirect('/');
  });

  router.get('/register', (req, res) => res.render('auth/register'));
  router.post('/register', (req, res) => {
    db.run("INSERT INTO users(username, password, email) VALUES(?, ?, ?)",
      [req.body.username, req.body.password, req.body.email], () => res.redirect('/auth/login'));
  });

  return router;
};
