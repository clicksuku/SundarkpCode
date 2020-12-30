const express = require('express')
const Program = require('../model/programModel')


exports.findAll = function(req, res) {
    Program.findAll(function(err, program) {
        console.log('program Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', program);
        res.send(program);
  });
};


exports.create = function(req, res) {
    const new_program = new Program(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
        Program.create(new_program, function(err, program) {
      if (err)
        res.send(err);

      res.json({error:false,message:"program added successfully!",data:program});
    });
    }
  };


  exports.findById = function(req, res) {
    Program.findById(req.params.id, function(err, program) {
        if (err)
          res.send(err);
          res.json(program);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
        Program.update(req.params.id, new Program(req.body), function(err, program) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'program successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
        Program.delete( req.params.id, function(err, program) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'program successfully deleted' });
      });
    };