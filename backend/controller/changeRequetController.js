const express = require('express')
const ChangeRequest = require('../model/changeRequestModel')


exports.findAll = function(req, res) {
    ChangeRequest.findAll(function(err, changeRequest) {
        console.log('changeRequest Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', changeRequest);
        res.send(changeRequest);
  });
};


exports.create = function(req, res) {
    const new_changeRequest = new ChangeRequest(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
        ChangeRequest.create(new_changeRequest, function(err, changeRequest) {
      if (err)
        res.send(err);

      res.json({error:false,message:"changeRequest added successfully!",data:changeRequest});
    });
    }
  };


  exports.findById = function(req, res) {
    ChangeRequest.findById(req.params.id, function(err, changeRequest) {
        if (err)
          res.send(err);
          res.json(changeRequest);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
        ChangeRequest.update(req.params.id, new ChangeRequest(req.body), function(err, changeRequest) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'changeRequest successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
        ChangeRequest.delete( req.params.id, function(err, changeRequest) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'changeRequest successfully deleted' });
      });
    };