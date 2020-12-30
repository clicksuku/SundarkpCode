const express = require('express')
const ExternalTeamsMaster = require('../model/externalTeamsMasterModel')


exports.findAll = function(req, res) {
    ExternalTeamsMaster.findAll(function(err, externalTeamsMaster) {
        console.log('ExternalTeamsMaster Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', externalTeamsMaster);
        res.send(externalTeamsMaster);
  });
};


exports.create = function(req, res) {
    const new_externalTeamsMaster = new ExternalTeamsMaster(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
      ExternalTeamsMaster.create(new_externalTeamsMaster, function(err, externalTeamsMaster) {
      if (err)
        res.send(err);
        res.json({error:false,message:"ExternalTeamsMaster added successfully!",data:externalTeamsMaster});
    });
    }
  };


  exports.findById = function(req, res) {
    ExternalTeamsMaster.findById(req.params.id, function(err, externalTeamsMaster) {
        if (err)
          res.send(err);
          res.json(externalTeamsMaster);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
          ExternalTeamsMaster.update(req.params.id, new ExternalTeamsMaster(req.body), function(err, externalTeamsMaster) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'ExternalTeamsMaster successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
    ExternalTeamsMaster.delete( req.params.id, function(err, externalTeamsMaster) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'ExternalTeamsMaster successfully deleted' });
      });
    };