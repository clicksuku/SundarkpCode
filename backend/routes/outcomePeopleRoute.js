const express = require('express')
const outcomePeopleRouter = express.Router();
const outcomePeopleContoller = require('../controller/outcomePeopleController')

outcomePeopleRouter.get('/', outcomePeopleContoller.findAll);
outcomePeopleRouter.post('/', outcomePeopleContoller.create);
outcomePeopleRouter.get('/:id', outcomePeopleContoller.findById);
outcomePeopleRouter.put('/:id', outcomePeopleContoller.update);
outcomePeopleRouter.delete('/:id', outcomePeopleContoller.delete);

module.exports = outcomePeopleRouter;