const express = require('express')
const Estimate = require('../model/estimateModel')


exports.findAll = function(req, res) {
    Estimate.findAll(function(err, estimate) {
        console.log('Estimate Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', estimate);
        res.send(estimate);
  });
};


exports.create = function(req, res) {
    const new_estimate = new Estimate(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
      new_estimate.PaymentsDomainsEstimates = JSON.stringify(new_estimate.PaymentsDomainsEstimates);
      new_estimate.ExternalTeamsEstimates = JSON.stringify(new_estimate.ExternalTeamsEstimates);
      Estimate.create(new_estimate, function(err, estimate) {
      if (err)
        res.send(err);

      res.json({error:false,message:"Estimate added successfully!",data:estimate});
    });
    }
  };


  exports.findById = function(req, res) {
    Estimate.findById(req.params.id, function(err, estimate) {
        if (err)
          res.send(err);
          res.json(estimate);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
          Estimate.update(req.params.id, new Estimate(req.body), function(err, estimate) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'Estimate successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
    Estimate.delete( req.params.id, function(err, estimate) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'Estimate successfully deleted' });
      });
    };