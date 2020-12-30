
const express = require('express')
const changeRequestRouter = express.Router();
const changeRequestController = require('../controller/changeRequetController')

changeRequestRouter.get('/', changeRequestController.findAll);
changeRequestRouter.post('/', changeRequestController.create);
changeRequestRouter.get('/:id', changeRequestController.findById);
changeRequestRouter.put('/:id', changeRequestController.update);
changeRequestRouter.delete('/:id', changeRequestController.delete); 

module.exports = changeRequestRouter;