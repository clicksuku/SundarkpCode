'use strict';
const pool = require('../util/db');

/*
CREATE TABLE `PeopleQuarterAvailability` (
  `PeopleId` int NOT NULL,
  `QuarterYear` varchar(25) DEFAULT NULL,
  `QuarterCapacityInDays` smallint DEFAULT '60',
  `QuarterReserveInDays` smallint DEFAULT '0',
  `QuarterLeavesInDays` smallint DEFAULT '0',
  `QuarterAvailableInDays` smallint DEFAULT '60',
  `SprintEngagementMatrix` varchar(250) DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LastUpdated` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

*/

var PeopleQuarter = function(peopleQuarter){
    this.PeopleId = peopleQuarter.PeopleId;
    this.QuarterYear = peopleQuarter.QuarterYear;
    
    this.QuarterCapacityInDays = peopleQuarter.QuarterCapacityInDays;
    this.QuarterReserveInDays = peopleQuarter.QuarterReserveInDays;
    this.QuarterLeavesInDays = peopleQuarter.QuarterLeavesInDays;
    this.QuarterAvailableInDays = peopleQuarter.QuarterAvailableInDays;
    this.SprintEngagementMatrix = peopleQuarter.SprintEngagementMatrix;

    this.Created = new Date();
    this.LastUpdated = new Date();
}

//Create

PeopleQuarter.create = function (newPeople, result) {
    pool.query("INSERT INTO PeopleQuarterAvailability set ?", 
    newPeople, function (err, res) {
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
PeopleQuarter.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM PeopleQuarterAvailability", function (err, res) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
        else{
            console.log('Peoples : ', res);
            result(null, res);
        }
    });
};

PeopleQuarter.findById = function (id, result) {
    pool.query("Select * from PeopleQuarterAvailability where PeopleId = ? ", id, function (err, res) {
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
CREATE TABLE `PeopleQuarterAvailability` (
  `PeopleId` int NOT NULL,
  `QuarterYear` varchar(25) DEFAULT NULL,
  `QuarterCapacityInDays` smallint DEFAULT '60',
  `QuarterReserveInDays` smallint DEFAULT '0',
  `QuarterLeavesInDays` smallint DEFAULT '0',
  `QuarterAvailableInDays` smallint DEFAULT '60',
  `SprintEngagementMatrix` varchar(250) DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LastUpdated` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

*/

PeopleQuarter.update = function(id, peopleQuarter, result){
    pool.query("UPDATE PeopleQuarterAvailability SET PeopleId=?, QuarterYear=?,QuarterCapacityInDays=?, QuarterReserveInDays=?, QuarterLeavesInDays = ?, QuarterAvailableInDays = ?, SprintEngagementMatrix = ?, LastUpdated=?   WHERE PeopleId = ?", 
        [peopleQuarter.PeopleId, peopleQuarter.QuarterYear,peopleQuarter.QuarterCapacityInDays, peopleQuarter.QuarterReserveInDays, peopleQuarter.QuarterLeavesInDays, peopleQuarter.QuarterAvailableInDays, peopleQuarter.SprintEngagementMatrix, peopleQuarter.LastUpdated,  PeopleId],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


PeopleQuarter.delete = function(id, result){
    pool.query("DELETE FROM PeopleQuarterAvailability WHERE PeopleId = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = PeopleQuarter;
