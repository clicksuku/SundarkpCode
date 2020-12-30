'use strict';
const pool = require('../util/db');

var ChangeRequestModel = function(changeRequest){
    this.ProgId = changeRequest.ProgId;
    this.Name = changeRequest.Name;
    this.Description = changeRequest.Description;
    this.Created = new Date();
    this.LastUpdated = new Date();
    this.TShirtSize = changeRequest.TShirtSize;
    this.Links = changeRequest.Links;
    this.Sprints = changeRequest.Sprints;
}

//Create

ChangeRequestModel.create = function (newChangeRequest, result) {
    pool.query("INSERT INTO changeRequest set ?", 
    newChangeRequest, function (err, res) {
        if(err) {
        console.log("error: ", err);
        result(err, null);
        }
        else{
        console.log(res.insertId);
        result(null, res.insertId);
        }
    });
};
    

// Find All
ChangeRequestModel.findAll = function (result) {
    console.log("Entered Find All")
    pool.query("SELECT * FROM changeRequest", function (err, res) {
        if(err) {
            console.log("error: ", err);
            result(err, null);
        }
        else{
            console.log('ChangeRequests : ', res);
            result(null, res);
        }
    });
};

ChangeRequestModel.findById = function (id, result) {
    pool.query("Select * from changeRequest where id = ? ", id, function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(err, null);
    }
    else{
      result(null, res);
        }
    });
};

ChangeRequestModel.update = function(id, changeRequest, result){
    pool.query("UPDATE changeRequest SET ProgId=?,Name=?,Description=?,LastUpdated=?, TShirtSize=?, Links=?, Sprints=? WHERE id = ?", 
        [changeRequest.ProgId,changeRequest.Name,changeRequest.Description,changeRequest.LastUpdated, changeRequest.TShirtSize, changeRequest.Color, changeRequest.Links, changeRequest.Sprints,
         changeRequest.CRs, id],  function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }else{
            result(null, res);
        }
    });
};


ChangeRequestModel.delete = function(id, result){
    pool.query("DELETE FROM changeRequest WHERE id = ?", [id], function (err, res) {
    if(err) {
      console.log("error: ", err);
      result(null, err);
    }
    else{
            result(null, res);
        }
    });
};

module.exports = ChangeRequestModel;
