
const express = require('express')
const externalTeamsMasterRouteRouter = express.Router();
const externalTeamsMasterRouteController = require('../controller/externalTeamsMasterController')

externalTeamsMasterRouteRouter.get('/', externalTeamsMasterRouteController.findAll);
externalTeamsMasterRouteRouter.post('/', externalTeamsMasterRouteController.create);
externalTeamsMasterRouteRouter.get('/:id', externalTeamsMasterRouteController.findById);
externalTeamsMasterRouteRouter.put('/:id', externalTeamsMasterRouteController.update);
externalTeamsMasterRouteRouter.delete('/:id', externalTeamsMasterRouteController.delete);

module.exports = externalTeamsMasterRouteRouter;