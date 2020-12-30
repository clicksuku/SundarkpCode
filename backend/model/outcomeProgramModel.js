'use strict';
const pool = require('../util/db');

var OutcomeProgram = function(outcomeprogram){
    this.OutcomeId = outcomeprogram.OutcomeId;
    this.ProgramId = outcomeprogram.ProgramId;
}

//Create

OutcomeProgram.create = function (newOutcomeProgram, result) {
    pool.query("INSERT INTO OutcomeProgramMapping set ?", 
    newOutcomeProgram, function (err) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
    });
};
    

// Find All
OutcomeProgram.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM OutcomeProgramMapping", function (err, res) {
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

OutcomeProgram.findById = function (programId, result) {
    pool.query("Select * from OutcomeProgramMapping where ProgramId = ? ", programId, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

OutcomeProgram.update = function(programId, outcomeprogram, result){
    pool.query("UPDATE OutcomeProgramMapping SET OutcomeId=?,ProgramId=? WHERE ProgramId = ?", [outcomeprogram.OutcomeId,outcomeprogram.ProgramId,
        programId],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


OutcomeProgram.delete = function(programId, result){
    pool.query("DELETE FROM OutcomeProgramMapping WHERE ProgramId = ?", [programId], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = OutcomeProgram;
