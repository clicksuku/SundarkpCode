const express = require('express')
const People = require('../model/peopleModel')

exports.findAll = function(req, res) {
    People.findAll(function(err, people) {
        console.log('people Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', people);
        res.send(people);
  });
};


exports.create = function(req, res) {
    const new_people = new People(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
        People.create(new_people, function(err, people) {
      if (err)
        res.send(err);

      res.json({error:false,message:"people added successfully!",data:people});
    });
    }
  };


  exports.findById = function(req, res) {
    People.findById(req.params.id, function(err, people) {
        if (err)
          res.send(err);
          res.json(people);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
        People.update(req.params.id, new People(req.body), function(err, people) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'people successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
        People.delete( req.params.id, function(err, people) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'people successfully deleted' });
      });
    };