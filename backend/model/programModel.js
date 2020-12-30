'use strict';
const pool = require('../util/db');

var Program = function(program){
    this.Name = program.Name;
    this.Description = program.Description;
    this.Created = new Date();
    this.LastUpdated = new Date();
    this.TShirtSize = program.TShirtSize;
    this.Links = program.Links;
    this.Color = program.Color;
    this.Sprints = program.Sprints;
    this.CRs = program.CRs;
}

//Create

Program.create = function (newProgram, result) {
    pool.query("INSERT INTO program set ?", 
    newProgram, function (err, res) {
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
Program.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM program", function (err, res) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
        else{
            console.log('Programs : ', res);
            result(null, res);
        }
    });
};

Program.findById = function (id, result) {
    pool.query("Select * from program where id = ? ", id, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

Program.update = function(id, program, result){
    pool.query("UPDATE program SET Name=?,Description=?,LastUpdated=?, TShirtSize=?, Color=?, Links=?, Sprints=?, CRs=?  WHERE id = ?", 
        [program.Name,program.Description,program.LastUpdated, program.TShirtSize, program.Color, program.Links, program.Sprints,
         program.CRs, id],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


Program.delete = function(id, result){
    pool.query("DELETE FROM program WHERE id = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = Program;
