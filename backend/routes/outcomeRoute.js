
const express = require('express')
const outcomeRouter = express.Router();
const outcomeController = require('../controller/outcomeController')

outcomeRouter.get('/', outcomeController.findAll);
outcomeRouter.post('/', outcomeController.create);
outcomeRouter.get('/:id', outcomeController.findById);
outcomeRouter.put('/:id', outcomeController.update);
outcomeRouter.delete('/:id', outcomeController.delete);

module.exports = outcomeRouter;