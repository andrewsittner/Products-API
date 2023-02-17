
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
                    feature: features.feature,
                    value: features.value
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
    let resultArray = [];
    let length = 0
    pool.query(`SELECT * FROM STYLES WHERE (product_id = ${req.params.id})`)
        .then((data) => {
            if (data.rows.length === 0) {
                res.status(200).json({
                    product_id: req.params.id,
                    results: resultArray
                })
            }
            length = data.rows.length;
            data.rows.map((style) => {
                pool.query(`SELECT * FROM PHOTOS WHERE (Style_Id = ${style.style_id})`)
                    .then(data => {
                        let stylePhotos = data.rows.map((photo) => {
                            return {
                                "thumbnail_url": photo.thumbnail_url,
                                "url": photo.url
                            }
                        })
                        style.photos = stylePhotos
                        pool.query(`SELECT * FROM SKUS WHERE (Style_Id = ${style.style_id})`)
                            .then(data => {
                                let def = false;
                                if (style.default_int === 1) {
                                    def = true
                                }
                                skus = {};
                                for (let i = 0; i < data.rows.length; i++) {
                                    skus[data.rows[i].skus_id] =
                                    {
                                        "quantity": data.rows[i].quantity,
                                        "size": data.rows[i].size
                                    }
                                }
                                style.skus = skus
                                resultObj = {
                                    'style_id': style.style_id,
                                    'name': style.name,
                                    'original_price': style.original_price,
                                    'sale_price': style.sale_price,
                                    'default?': def,
                                    'photos': style.photos,
                                    'skus': style.skus
                                }
                                resultArray.push(resultObj)
                                if (resultArray.length === length) {
                                    res.status(200).json(
                                        resultArray
                                    )
                                }
                            })
                    })
            })

        })
        .catch(err => console.log('error in getProductsWithId', err))
}

const getProductsRelated = (req, res) => {
    pool.query(`SELECT * FROM RELATED WHERE (Current_product_id = ${req.params.id})`)
        .then((data) => {
            relatedArray = [];
            for (let i = 0; i < data.rows.length; i++) {
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