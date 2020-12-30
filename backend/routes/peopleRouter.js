const express = require('express')
const peopleRouter = express.Router();
const peopleController = require('../controller/peopleController')

peopleRouter.get('/', peopleController.findAll);
peopleRouter.post('/', peopleController.create);
peopleRouter.get('/:id', peopleController.findById);
peopleRouter.put('/:id', peopleController.update);
peopleRouter.delete('/:id', peopleController.delete);

module.exports = peopleRouter;