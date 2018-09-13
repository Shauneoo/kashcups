const express = require('express');
const router = express.Router();
const mysql = require('mysql')


fetchUserID = (nfc, callback) => {
  connection.query(`SELECT id FROM cups WHERE nfc = "${nfc}"`,  function(err, rows) {
    if (err) {
      callback(err, null);
    } else {
      callback(null, rows[0].id);
    }
  });
}

fetchUsersIDS = (nfc1, nfc2, callback) => {
  connection.query(`SELECT id FROM cups WHERE nfc="${nfc1}" OR nfc="${nfc2}"`,  function(err, rows) {
    if (err) {
      callback(err, null);
    } else
      callback(null, rows);
  });
}

updatePoints = (cupID, type, callback) => {
  let multiplier;
  switch (type) {
    case "vote":
      multiplier = 5;
      break;
    case "interaction":
      multiplier = 10;
      break;
    default:
      multiplier = 1;

  }
  connection.query(`UPDATE cups SET points = points+"${multiplier}" WHERE id="${cupID}"`,  function(err, rows) {
    if (err) {
      callback(err, null);
    } else
      callback(null, rows[0]);
  });
}

logInteractionEvent = (cup_id1,cup_id2,type,station_id, callback) => {
  connection.query(
    `INSERT INTO eventlog( cup_id1, cup_id2, type, station_id, timestamp) VALUES("${cup_id1}","${cup_id2}","${type}","${station_id}",current_timestamp)`,  function(err, rows) {
    if (err) {
      callback(err, null);
    } else
      callback(null, rows[0]);
      // console.log(rows)
  });
}

logVotingEvent = (cup_id,type,vote,station_id, callback) => {
  connection.query(
    `INSERT INTO eventlog(cup_id1, type, vote, station_id, timestamp) VALUES("${cup_id}", "${type}", "${vote}", "${station_id}", current_timestamp)`,  function(err, rows) {
    if (err) {
      callback(err, null);
    } else
      callback(null, rows[0]);
  });
}

//config credentials
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  // password: 'root',
  database: 'kashcups'
});

//print connection status
connection.connect(function (err) {
  if (!err) {
    console.log("Database is connected ... \n\n");
  } else {
    console.log("Error connecting database ... \n\n");
  }
});

/* GET home page. */
router.get('/', (req, res) => {
  res.render('index', { title: 'kashcups' });
});

// GET cup info page
router.get('/cupsinfo', (req, res) => {
  connection.query('SELECT id, status, points, (SELECT COUNT(id) FROM cups WHERE cups.id = cups.id) AS total FROM `cups` WHERE 1 ORDER BY id',
    function (err, rows, fields) {
      if (!err) {
        // console.log(rows)
        res.json(rows);
      }
      else {
        connection.end();
        console.log('Error while performing Query.');
      }
  });
});

//interaction
/*
  2 stations of double bases
  int1
  int2
*/
router.put('/modify', (req, res) => {
  let cupID1, cupID2;
  fetchUsersIDS(req.body.nfc1,req.body.nfc2, (err, content) => {
    if (err) {
      return console.log(err)
      res.send("Incorrect cup ID please try again")
    } else {
      cupID1 = content[0].id;
      cupID2 = content[1].id;
      console.log("Successfully retreieved ids: Cup1 " +cupID1+" Cup2 "+cupID2)

      //add points to cups accounts
      updatePoints(cupID1, req.body.type, (err, content) => {
        if (err) return console.log(err);
        else {
          console.log("Successfully incremented points on "+cupID1)
        }
      });
      updatePoints(cupID2, req.body.type, (err, content) => {
        if (err) return console.log(err);
        else {
          console.log("Successfully incremented points on "+cupID2)
        }
      });

      // log event
      // [params]: cup_id1, cup_id2, type,station_id
      logInteractionEvent(cupID1,cupID2,req.body.type,req.body.station_id, (err, content) => {
        if (err) return console.log(err);
        else {
          console.log("Successfully logged event")
        }
      });
    }
  });
  res.send(200)
});

//voting
/*
  2 stations of 3 single bases
  v1a,v1b,v1c
  v2a,v2b,v2c
*/
router.post('/voting', (req, res) => {
  let cupID;
  fetchUserID(req.body.nfc, (err, content) => {
    if (err) {
      console.log(err);
    } else {
      cupID = content;
      console.log("Successfully retreieved id:" +cupID)

      //add points to cup account
      updatePoints(cupID, req.body.type, (err, content) => {
        if (err) return console.log(err);
        else {
          console.log("Successfully incremented points")
        }
      });

      //log event
      //[params]: cup_id type,vote,station_id
      logVotingEvent(cupID,req.body.type,req.body.station_id,req.body.station_id, (err, content) => {
        if (err) return console.log(err);
        else {
          console.log("Successfully logged event")
        }
      });


    }
  });
  res.send(200)
});

// data export route
router.post('/export', (req, res) => {
  fetchUserData(req.body.id, (err, content) => {
    if (err) return console.log(err);
    else {
      console.log("Successfully retreieved user data")
      console.log(content);
      if (content) {
        res.send([content[0], content[1]])
      } else {
        res.send(400)
      }
    }
  });
});


fetchUserData = (id, callback) => {
  connection.query(`SELECT points, id FROM cups WHERE id = "${id}"`, (err, rows) => {
      if (err) {
        callback(err, null);
      } else {
        if (rows.length) {
          callback(null, [rows[0].id, rows[0].points]);
        } else {
          callback(err,null)
        }
      }
    });
}

module.exports = router;
