
const express = require('express')
const estimateRouter = express.Router();
const estimateController = require('../controller/estimateController')

estimateRouter.get('/', estimateController.findAll);
estimateRouter.post('/', estimateController.create);
estimateRouter.get('/:id', estimateController.findById);
estimateRouter.put('/:id', estimateController.update);
estimateRouter.delete('/:id', estimateController.delete);

module.exports = estimateRouter;