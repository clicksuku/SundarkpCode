'use strict';
const pool = require('../util/db');

var People = function(people){
    this.Name = people.Name;
    this.PrimarySkillSet = people.PrimarySkillSet;
    this.SecondarySkillSet = people.SecondarySkillSet;
    this.QuarterYear = people.QuarterYear;
    this.QuarterCapacityInDays= people.QuarterCapacityInDays;
    this.QuarterReserveInDays= people.QuarterReserveInDays;
    this.QuarterLeavesInDays= people.QuarterLeavesInDays;
    this.QuarterAvailableInDays= people.QuarterAvailableInDays;
    this.SpringEngagementMatrix= people.SpringEngagementMatrix;
    this.Created = new Date();
    this.LastUpdated = new Date();
}

var pick = function (obj, props) {

	'use strict';

	// Make sure object and properties are provided
	if (!obj || !props) return;

	// Create new object
	var picked = {};

	// Loop through props and push to new object
	props.forEach(function(prop) {
		picked[prop] = obj[prop];
	});

	// Return new object
	return picked;

};



//Create
People.create = function (newPeople, result) {
    var peopleCore = pick(newPeople, ['Name','PrimarySkillSet', 'SecondarySkillSet', 'Created', 'LastUpdated']);
    
    pool.query("INSERT INTO people set ?", 
    peopleCore ,function (err, res) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
        else{
            console.log(res.insertId);

            var peopleAvailability = pick(newPeople, ['QuarterYear','QuarterCapacityInDays', 'QuarterReserveInDays','QuarterLeavesInDays', 'QuarterAvailableInDays', 'SprintEngagementMatrix' ,'Created', 'LastUpdated']);
            peopleAvailability['PeopleId'] = res.insertId;

            pool.query("INSERT INTO PeopleQuarterAvailability set ?", 
            peopleAvailability, function (err, res) {

            });

            result(null, res.insertId);
        }
    });
};
    

// Find All
People.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM people JOIN PeopleQuarterAvailability on people.Id=PeopleQuarterAvailability.PeopleId", function (err, res) {
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

People.findById = function (id, result) {
    pool.query("SELECT * FROM people JOIN PeopleQuarterAvailability on people.Id=PeopleQuarterAvailability.PeopleId where id = ? ", id, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

People.update = function(id, people, result){
    pool.query("UPDATE people SET Name=?,Description=?, LastUpdated=?, PrimarySkillSet = ?, SecondarySkillSet = ?   WHERE id = ?", 
        [people.Name,people.Description, people.LastUpdated, people.PrimarySkillSet, people.SecondarySkillSet,  id],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


People.delete = function(id, result){
    pool.query("DELETE FROM people WHERE id = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            pool.query("DELETE FROM PeopleQuarterAvailability WHERE PeopleId = ?", [id], function (err, res) {});
            result(null, res);
        }
    });
};

module.exports = People;
