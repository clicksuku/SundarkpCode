'use strict';
const pool = require('../util/db');

var Outcome = function(outcome){
    this.Name = outcome.Name;
    this.Description = outcome.Description;
    this.Created = new Date();
    this.LastUpdated = new Date();
}

//Create

Outcome.create = function (newOutcome, result) {
    pool.query("INSERT INTO outcome set ?", 
    newOutcome, function (err, res) {
        if(err) {
        console.log("error: ", err);
        result(err, null);
        }
        else{
        console.log(res.insertId);
        result(null, res.insertId);
        }
    });
};
    

// Find All
Outcome.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM outcome", function (err, res) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
        else{
            console.log('Outcomes : ', res);
            result(null, res);
        }
    });
};

Outcome.findById = function (id, result) {
    pool.query("Select * from outcome where id = ? ", id, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

Outcome.update = function(id, outcome, result){
    pool.query("UPDATE outcome SET Name=?,Description=?,LastUpdated=? WHERE id = ?", [outcome.Name,outcome.Description,
        outcome.LastUpdated, id],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


Outcome.delete = function(id, result){
    pool.query("DELETE FROM outcome WHERE id = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = Outcome;
