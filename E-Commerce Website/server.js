const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const db = new sqlite3.Database('./db.sqlite');

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({ secret: 'secret-key', resave: false, saveUninitialized: true }));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes
app.use('/auth', require('./routes/auth')(db));
app.use('/', require('./routes/products')(db));
app.use('/cart', require('./routes/cart')(db));
app.use('/checkout', require('./routes/checkout')(db));
app.use('/account', require('./routes/account')(db));
app.use('/support', require('./routes/support')(db));
app.use('/admin', require('./routes/admin')(db));

// Start server
app.listen(3000, () => console.log('Server running on http://localhost:3000'));

const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const db = new sqlite3.Database('./db.sqlite');

// Simple test route
app.get('/', (req, res) => {
  res.send('E-commerce server is running!');
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
