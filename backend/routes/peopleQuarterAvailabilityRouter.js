const express = require('express')
const peopleQuarterAvailabilityRouter = express.Router();
const peopleQuarterAvailabilityContoller = require('../controller/peopleQuarterAvailabilityController')

peopleQuarterAvailabilityRouter.get('/', peopleQuarterAvailabilityContoller.findAll);
peopleQuarterAvailabilityRouter.post('/', peopleQuarterAvailabilityContoller.create);
peopleQuarterAvailabilityRouter.get('/:id', peopleQuarterAvailabilityContoller.findById);
peopleQuarterAvailabilityRouter.put('/:id', peopleQuarterAvailabilityContoller.update);
peopleQuarterAvailabilityRouter.delete('/:id', peopleQuarterAvailabilityContoller.delete);

module.exports = peopleQuarterAvailabilityRouter;