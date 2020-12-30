const express = require('express')
const OutcomeProgram = require('../model/outcomeProgramModel')

exports.findAll = function(req, res) {
  OutcomeProgram.findAll(function(err, outcomeprogram) {
        console.log('OutcomeProgram Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', outcomeprogram);
        res.send(outcomeprogram);
  });
};


exports.create = function(req, res) {
    //handles null error
    const outcomeId = req.body.OutcomeId;
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
        let programs = req.body.Program;
        
        for(let program of programs)
        {
          let newOutcomeProgram={};
          newOutcomeProgram["OutcomeId"] = outcomeId;
          newOutcomeProgram["ProgramId"] = program["ProgramId"];
          
          OutcomeProgram.create(newOutcomeProgram, function(err) {
            if (err)
                res.send(err);

          });
        }        
        
    }
    res.json({error:false,message:"Mapping added successfully!"});  
  };


  exports.findById = function(req, res) {
    OutcomeProgram.findById(req.params.id, function(err, outcomeprogram) {
        if (err)
          res.send(err);
          res.json(outcomeprogram);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
        OutcomeProgram.update(req.params.id, new OutcomeProgram(req.body), function(err, outcomeprogram) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'OutcomeProgram successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
      OutcomeProgram.delete( req.params.id, function(err, outcomeprogram) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'people successfully deleted' });
      });
    };