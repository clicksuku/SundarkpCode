const express = require('express')
const ExternalOrgMaster = require('../model/externalOrgMasterModel')


exports.findAll = function(req, res) {
    ExternalOrgMaster.findAll(function(err, externalOrgMaster) {
        console.log('ExternalOrgMaster Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', externalOrgMaster);
        res.send(externalOrgMaster);
  });
};


exports.create = function(req, res) {
    const new_orgMaster = new ExternalOrgMaster(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
      ExternalOrgMaster.create(new_orgMaster, function(err, externalOrgMaster) {
      if (err)
        res.send(err);

      res.json({error:false,message:"ExternalOrgMaster added successfully!",data:externalOrgMaster});
    });
    }
  };


  exports.findById = function(req, res) {
    ExternalOrgMaster.findById(req.params.id, function(err, externalOrgMaster) {
        if (err)
          res.send(err);
          res.json(externalOrgMaster);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
          ExternalOrgMaster.update(req.params.id, new ExternalOrgMaster(req.body), function(err, externalOrgMaster) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'ExternalOrgMaster successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
    ExternalOrgMaster.delete( req.params.id, function(err, externalOrgMaster) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'ExternalOrgMaster successfully deleted' });
      });
    };