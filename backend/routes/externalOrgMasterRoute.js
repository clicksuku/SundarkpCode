
const express = require('express')
const externalOrgMasterRouter = express.Router();
const externalOrgMasterController = require('../controller/externalOrgMasterController')

externalOrgMasterRouter.get('/', externalOrgMasterController.findAll);
externalOrgMasterRouter.post('/', externalOrgMasterController.create);
externalOrgMasterRouter.get('/:id', externalOrgMasterController.findById);
externalOrgMasterRouter.put('/:id', externalOrgMasterController.update);
externalOrgMasterRouter.delete('/:id', externalOrgMasterController.delete);

module.exports = externalOrgMasterRouter;