'use strict';
const pool = require('../util/db');

var PaymentsDomains = function(paymentsTeamMaster){
    this.Name = paymentsTeamMaster.Name;
    this.Description = paymentsTeamMaster.Description;
    this.Created = new Date();
    this.LastUpdated = new Date();
}

//Create

PaymentsDomains.create = function (newOrgMaster, result) {
    pool.query("INSERT INTO PaymentsDomainsMaster set ?", 
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
PaymentsDomains.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM PaymentsDomainsMaster", function (err, res) {
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

PaymentsDomains.findById = function (id, result) {
    pool.query("Select * from PaymentsDomainsMaster where id = ? ", id, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

PaymentsDomains.update = function(id, paymentsTeamMaster, result){
    pool.query("UPDATE PaymentsDomainsMaster SET Name=?, Description=?, LastUpdated=? WHERE id = ?", [paymentsTeamMaster.Name, paymentsTeamMaster.Description,
        paymentsTeamMaster.LastUpdated, id],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


PaymentsDomains.delete = function(id, result){
    pool.query("DELETE FROM PaymentsDomainsMaster WHERE id = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = PaymentsDomains;
