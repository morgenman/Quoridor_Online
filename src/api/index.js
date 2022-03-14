const express = require("express");
require("dotenv").config();
const app = express();
const mysql = require("mysql2");
const cors = require("cors");

app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});


// Sending data to the database
app.post("/add", (req, res) => {
  const id = req.body.id;
  const aid = req.body.aid;
  const value = req.body.value;
  const date = req.body.date;

  db.query(
    "insert into games (gamestate, player1, player2) values (?,?,?,?)",
    [id, aid, value, date],
    (err, result) => {
      if (err) {
        res.send(err);
      } else {
        res.send("Values Added");
      }
    }
  );
});

// Get data from the databse
app.get("/gameID", (req, res) => {
  //res.send("Testing");
  db.query(
    "SELECT * from games",
    (err, result) => {
      if (err) {
        res.send(err);
      } else {
        res.send(result);
      }
    }
  );
});



// Get data using ID
app.get("/report_name", (req, res) => {
  var sql = "select X from games where game_id ="
  sql = sql.concat(req.query.gameid);
  //console.log(sql);
  db.query(sql,
    (err, result) => {
      if (err) {
        res.send(err);
      } else {
        res.send(result[0].attribute_desc);
      }
    }
  );
});

app.listen(8080, () => {
  console.log("API is listening on port 9696:8080");
});
