'use strict';

const mysql = require('mysql');

const pool = mysql.createPool({
  connectionLimit : 10,
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'Estimates'
});

module.exports = pool;