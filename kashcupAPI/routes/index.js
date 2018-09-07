var express = require('express');
var router = express.Router();
var mysql = require('mysql')

var connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'kashcups'
});

connection.connect(function (err) {
  if (!err) {
    console.log("Database is connected ... \n\n");
  } else {
    console.log("Error connecting database ... \n\n");
  }
});
/* GET home page. */

router.get('/', function (req, res) {
  res.render('index', { title: 'Express' });
});

router.get('/cupsinfo', function (req, res) {
  connection.query('SELECT id, status, (SELECT COUNT(id) FROM activities WHERE activities.cup_id1 = cups.id) AS total FROM `cups` WHERE 1 ORDER BY id',
    function (err, rows, fields) {
      if (!err){
        res.json(rows);
      }
      else{
        connection.end();
        throw err;
        console.log('Error while performing Query.');
      }
    });
});

//modify cup (id, status)
router.post('/modify', function (req, res) {
  //sql query
  Test
});

//nuke option
router.post('/modify', function (req, res) {
  //sql query
  test
});

// data export route


module.exports = router;
