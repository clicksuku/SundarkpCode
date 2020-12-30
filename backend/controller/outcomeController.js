const express = require('express')
const Outcome = require('../model/outcomeModel')


exports.findAll = function(req, res) {
    Outcome.findAll(function(err, outcome) {
        console.log('Outcome Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', outcome);
        res.send(outcome);
  });
};


exports.create = function(req, res) {
    const new_outcome = new Outcome(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
      Outcome.create(new_outcome, function(err, outcome) {
      if (err)
        res.send(err);

      res.json({error:false,message:"Outcome added successfully!",data:outcome});
    });
    }
  };


  exports.findById = function(req, res) {
    Outcome.findById(req.params.id, function(err, outcome) {
        if (err)
          res.send(err);
          res.json(outcome);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
          Outcome.update(req.params.id, new Outcome(req.body), function(err, outcome) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'Outcome successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
    Outcome.delete( req.params.id, function(err, outcome) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'Outcome successfully deleted' });
      });
    };