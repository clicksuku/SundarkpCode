'use strict';
const pool = require('../util/db');

/*
`ProgramId` int NOT NULL,
  `PaymentsEstimates` json DEFAULT NULL,
  `ExternalTeamsEstimates` json DEFAULT NULL,
  `PaymentsTShirtSize` varchar(5) DEFAULT 'M',
  `PaymentsSprints` int DEFAULT '10',
  `Created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LastUpdated` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `Revision` int DEFAULT NULL,
  `ExternalTeamsTShirtSize` varchar(5) DEFAULT 'M',
  `ExternalTeamsSprints` int DEFAULT '10',

*/

var Estimate = function(estimate){
    this.ProgramId = estimate.ProgramId;
    this.PaymentsDomainsEstimates = estimate.PaymentsDomainsEstimates;
    this.ExternalTeamsEstimates = estimate.ExternalTeamsEstimates;
    this.PaymentsTShirtSize = estimate.PaymentsTShirtSize;
    this.PaymentsSprints = estimate.PaymentsSprints;
    this.ExternalTeamsTShirtSize = estimate.ExternalTeamsTShirtSize;
    this.ExternalTeamsSprints = estimate.ExternalTeamsSprints;
    this.Created = new Date();
    this.LastUpdated = new Date();
    this.Revision = estimate.Revision;
}

//Create

Estimate.create = function (newEstimate, result) {
    pool.query("INSERT INTO estimates set ?", 
    newEstimate, function (err, res) {
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
Estimate.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM estimates", function (err, res) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
        else{
            console.log('Estimates : ', res);
            result(null, res);
        }
    });
};

Estimate.findById = function (id, result) {
    pool.query("Select * from estimates where ProgramId = ? ", id, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

/*

`ProgramId` int NOT NULL,
  `PaymentsDomainsEstimates` json DEFAULT NULL,
  `ExternalTeamsEstimates` json DEFAULT NULL,
  `PaymentsTShirtSize` varchar(5) DEFAULT 'M',
  `PaymentsSprints` int DEFAULT '10',
  `Created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LastUpdated` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `Revision` int DEFAULT NULL,
  `ExternalTeamsTShirtSize` varchar(5) DEFAULT 'M',
  `ExternalTeamsSprints` int DEFAULT '10',

*/


Estimate.update = function(id, estimate, result){
    pool.query("UPDATE estimates SET ProgramId=?,PaymentsDomainsEstimates=?,ExternalTeamsEstimates=?, PaymentsTShirtSize=?, PaymentsSprints=?, ExternalTeamsTShirtSize = ?, ExternalTeamsSprints = ?, LastUpdated=?, Revision=? WHERE ProgramId = ?", 
    [estimate.ProgramId,estimate.PaymentsDomainsEstimates, estimate.ExternalTeamsEstimates, estimate.PaymentsTShirtSize, estimate.PaymentsSprints, estimate.ExternalTeamsTShirtSize, estimate.ExternalTeamsSprints,
        estimate.LastUpdated, estimate.Revision, id],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


Estimate.delete = function(id, result){
    pool.query("DELETE FROM estimates WHERE ProgramId = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = Estimate;
