
const express = require('express')
const programRouter = express.Router();
const programController = require('../controller/programController')

programRouter.get('/', programController.findAll);
programRouter.post('/', programController.create);
programRouter.get('/:id', programController.findById);
programRouter.put('/:id', programController.update);
programRouter.delete('/:id', programController.delete);

module.exports = programRouter;