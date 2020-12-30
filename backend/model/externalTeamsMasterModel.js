'use strict';
const pool = require('../util/db');

var ExternalTeamsMaster = function(ExternalTeamsMaster){
    this.OrgId = ExternalTeamsMaster.OrgId;
    this.Name = ExternalTeamsMaster.Name;
    this.Description = ExternalTeamsMaster.Description;
    this.Created = new Date();
    this.LastUpdated = new Date();
}

//Create

ExternalTeamsMaster.create = function (newOrgMaster, result) {
    pool.query("INSERT INTO ExternalTeamsMaster set ?", 
    newOrgMaster, function (err, res) {
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
ExternalTeamsMaster.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM ExternalTeamsMaster", function (err, res) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
        else{
            console.log('OrgMasters : ', res);
            result(null, res);
        }
    });
};

ExternalTeamsMaster.findById = function (id, result) {
    pool.query("Select * from ExternalTeamsMaster where id = ? ", id, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

ExternalTeamsMaster.update = function(id, ExternalTeamsMaster, result){
    pool.query("UPDATE ExternalTeamsMaster SET OrgId=?, Name=?, Description=?,LastUpdated=? WHERE id = ?", [ExternalTeamsMaster.OrgId,ExternalTeamsMaster.Name, ExternalTeamsMaster.Description,
        ExternalTeamsMaster.LastUpdated, id],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


ExternalTeamsMaster.delete = function(id, result){
    pool.query("DELETE FROM ExternalTeamsMaster WHERE id = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = ExternalTeamsMaster;
