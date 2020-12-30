const express = require('express')
const OutcomePeople = require('../model/outcomePeopleModel')

exports.findAll = function(req, res) {
  OutcomePeople.findAll(function(err, outcomepeople) {
        console.log('OutcomePeople Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', outcomepeople);
        res.send(outcomepeople);
  });
};


exports.create = function(req, res) {
    //handles null error
    const outcomeId = req.body.OutcomeId;
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
        let peoples = req.body.People;
        
        for(let people of peoples)
        {
          let newOutcomePeople={};
          newOutcomePeople["OutcomeId"] = outcomeId;
          newOutcomePeople["PeopleId"] = people["PeopleId"];
          newOutcomePeople["Allocation"] = people["Allocation"];
          
          OutcomePeople.create(newOutcomePeople, function(err) {
            if (err)
                res.send(err);

          });
        }        
    }
    res.json({error:false,message:"Mapping added successfully!"});
  };


  exports.findById = function(req, res) {
    OutcomePeople.findById(req.params.id, function(err, outcomepeople) {
        if (err)
          res.send(err);
          res.json(outcomepeople);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
        OutcomePeople.update(req.params.id, new OutcomePeople(req.body), function(err, outcomepeople) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'OutcomePeople successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
      OutcomePeople.delete( req.params.id, function(err, outcomepeople) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'people successfully deleted' });
      });
    };