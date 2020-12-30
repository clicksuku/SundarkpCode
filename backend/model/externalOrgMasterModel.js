'use strict';
const pool = require('../util/db');

var ExternalOrgMaster = function(externalOrgMaster){
    this.Name = externalOrgMaster.Name;
    this.Description = externalOrgMaster.Description;
    this.Created = new Date();
    this.LastUpdated = new Date();
}

//Create

ExternalOrgMaster.create = function (newOrgMaster, result) {
    pool.query("INSERT INTO ExternalOrgMaster set ?", 
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
ExternalOrgMaster.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM ExternalOrgMaster", function (err, res) {
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

ExternalOrgMaster.findById = function (id, result) {
    pool.query("Select * from ExternalOrgMaster where id = ? ", id, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

ExternalOrgMaster.update = function(id, externalOrgMaster, result){
    pool.query("UPDATE ExternalOrgMaster SET Name=?, Description=?,LastUpdated=? WHERE id = ?", [externalOrgMaster.Name, externalOrgMaster.Description,
        externalOrgMaster.LastUpdated, id],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


ExternalOrgMaster.delete = function(id, result){
    pool.query("DELETE FROM externalOrgMaster WHERE id = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = ExternalOrgMaster;
