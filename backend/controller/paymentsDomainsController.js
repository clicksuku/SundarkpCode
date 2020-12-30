const express = require('express')
const PaymentsDomain = require('../model/paymentsDomainsModel')


exports.findAll = function(req, res) {
  PaymentsDomain.findAll(function(err, paymentsDomains) {
        console.log('Payments Domain Controller')
        
        if (err)
          res.send(err);
        
        console.log('res', paymentsDomains);
        res.send(paymentsDomains);
  });
};


exports.create = function(req, res) {
    const new_paymentsDomain = new PaymentsDomain(req.body);
   //handles null error
    if(Object.keys(req.body).length === 0){
      res.status(400).send({ error:true, message: 'Please provide all required field' });
    }else{
      PaymentsDomain.create(new_paymentsDomain, function(err, paymentDomain) {
      if (err)
        res.send(err);

      res.json({error:false,message:"Payments Domain added successfully!",data:paymentDomain});
    });
    }
  };


  exports.findById = function(req, res) {
    PaymentsDomain.findById(req.params.id, function(err, paymentDomain) {
        if (err)
          res.send(err);
          res.json(paymentDomain);
      });
    };

    exports.update = function(req, res) {
      if(req.body.constructor === Object && Object.keys(req.body).length === 0){
        res.status(400).send({ error:true, message: 'Please provide all required field' });
      }else{
        PaymentsDomain.update(req.params.id, new PaymentsDomain(req.body), function(err, paymentDomain) {
          if (err)
            res.send(err);
          res.json({ error:false, message: 'Payments Domain successfully updated' });
        });
      }
    };

    exports.delete = function(req, res) {
      PaymentsDomain.delete( req.params.id, function(err, paymentDomain) {
        if (err)
          res.send(err);
        res.json({ error:false, message: 'Payments Domain successfully deleted' });
      });
    };