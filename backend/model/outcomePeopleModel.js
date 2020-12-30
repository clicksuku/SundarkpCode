'use strict';
const pool = require('../util/db');

var OutcomePeople = function(outcomepeople){
    this.OutcomeId = outcomepeople.OutcomeId;
    this.PeopleId = outcomepeople.PeopleId;
    this.Allocation = outcomepeople.Allocation;
}

//Create

OutcomePeople.create = function (newOutcomePeople, result) {
    pool.query("INSERT INTO OutcomePeopleMapping set ?", 
    newOutcomePeople, function (err) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
    });
};
    

// Find All
OutcomePeople.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM OutcomePeopleMapping", function (err, res) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
        else{
            console.log('Outcomes People Mapping : ', res);
            result(null, res);
        }
    });
};

OutcomePeople.findById = function (peopleId, result) {
    pool.query("Select * from OutcomePeopleMapping where PeopleId = ? ", peopleId, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

OutcomePeople.update = function(peopleId, outcomepeople, result){
    pool.query("UPDATE OutcomePeopleMapping SET OutcomeId=?,PeopleId=?,Allocation=? WHERE PeopleId = ?", [outcomepeople.OutcomeId,outcomepeople.PeopleId,
        outcomepeople.Allocation, peopleId],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


OutcomePeople.delete = function(peopleId, result){
    pool.query("DELETE FROM OutcomePeopleMapping WHERE PeopleId = ?", [peopleId], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = OutcomePeople;
