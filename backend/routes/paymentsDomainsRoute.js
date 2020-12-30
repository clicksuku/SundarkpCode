
const express = require('express')
const paymentDomainsRouter = express.Router();
const paymentsDomainsController = require('../controller/paymentsDomainsController')

paymentDomainsRouter.get('/', paymentsDomainsController.findAll);
paymentDomainsRouter.post('/', paymentsDomainsController.create);
paymentDomainsRouter.get('/:id', paymentsDomainsController.findById);
paymentDomainsRouter.put('/:id', paymentsDomainsController.update);
paymentDomainsRouter.delete('/:id', paymentsDomainsController.delete);

module.exports = paymentDomainsRouter;