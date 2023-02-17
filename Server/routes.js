const { Router } = require('express');
const controller = require('./controller');


const router = Router();

router.get('/', controller.getProducts);
router.get('/:id', controller.getProductsWithId);
router.get('/:id/styles', controller.getProductsStyle);
router.get('/:id/related', controller.getProductsRelated);



module.exports = router; 

