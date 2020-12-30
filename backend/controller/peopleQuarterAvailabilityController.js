const express = require('express')
const PeopleQuarterAvailability = require('../model/peopleQuarterAvailabilityModel')

exports.findAll = function(req, res) {
  PeopleQuarterAvailability.findAll(function(err, people) {
        console.log('people Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', people);
        res.send(people);
  });
};


exports.create = function(req, res) {
    const new_people_quarter = new PeopleQuarterAvailability(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
        PeopleQuarterAvailability.create(new_people_quarter, function(err, peopleQuarterMatrix) {
      if (err)
        res.send(err);

      res.json({error:false,message:"people added successfully!",data:peopleQuarterMatrix});
    });
    }
  };


  exports.findById = function(req, res) {
    PeopleQuarterAvailability.findById(req.params.id, function(err, peopleQuarterMatrix) {
        if (err)
          res.send(err);
          res.json(peopleQuarterMatrix);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
        PeopleQuarterAvailability.update(req.params.id, new PeopleQuarterAvailability(req.body), function(err, peopleQuarter) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'PeopleQuarterMatrix successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
      PeopleQuarterAvailability.delete( req.params.id, function(err, peopleQuarterMatrix) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'PeopleQuarterMatrix successfully deleted' });
      });
    };