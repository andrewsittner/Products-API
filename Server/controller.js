
const pool = require('../Database/db'); 

const getProducts = (req, res) => {
    let count = req.query.count || 5
    let page = req.query.page || 1
    let sql = `product_id <= ${count * page} and product_id >= ${(count * page) - count}` 
    pool.query(`SELECT * FROM PRODUCTS WHERE (${sql}); `)
    .then((data) => {
       res.status(200).json(data.rows)
    })
    .catch(err => console.log(err, 'err in getProducts'))
};

const getProductsWithId = (req, res) => { 
    pool.query(`SELECT * FROM FEATURES WHERE (product_id = ${req.params.id})`)
    .then((data) => {
        let productFeatures = data.rows.map((features) => {
            return {
                feature : features.feature, 
                value : features.value
            }
        })
        pool.query(`SELECT * FROM PRODUCTS WHERE (product_id = ${req.params.id})`)
        .then((data) => {
            data.rows.features = productFeatures
            res.status(200).json(data.rows)
        }) 
        .catch(err => console.log('error in getProductsWithId get products query', err))
    })
    .catch(err => console.log('error in getProductsWithId get features query', err))
};

const getProductsStyle = (req, res) => {
    pool.query(`SELECT * FROM STYLES WHERE (product_id = ${req.params.id})`)
    .then((data) => {
        let styleObj = {
            product_id : req.params.id,
            results: []
        }
        console.log(data.rows, req.params.id)
        res.status(200).json(data.rows)
    })
    .catch(err => console.log('error in getProductsWithId', err))
}

const getProductsRelated = (req, res) => {
    pool.query(`SELECT * FROM RELATED WHERE (Current_product_id = ${req.params.id})`)
    .then((data) => {
        relatedArray = [];
        for(let i = 0; i < data.rows.length; i++) {
            relatedArray.push(data.rows[i].related_products_id) 
        }
        res.status(200).json(relatedArray)
    })
    .catch(err => console.log('error in getProductsWithId', err))
}



module.exports = {
    getProducts, 
    getProductsWithId,
    getProductsStyle,
    getProductsRelated
}