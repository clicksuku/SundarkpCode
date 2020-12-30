const express = require('express')
const outcomeProgramRouter = express.Router();
const outcomeProgramController = require('../controller/outcomeProgramController')

outcomeProgramRouter.get('/', outcomeProgramController.findAll);
outcomeProgramRouter.post('/', outcomeProgramController.create);
outcomeProgramRouter.get('/:id', outcomeProgramController.findById);
outcomeProgramRouter.put('/:id', outcomeProgramController.update);
outcomeProgramRouter.delete('/:id', outcomeProgramController.delete);

module.exports = outcomeProgramRouter;