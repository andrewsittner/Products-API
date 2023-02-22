require('dotenv').config()
const express = require('express');
const app = express();
const routes = require('./routes');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.json({message: 'welcome to server route test page'})
});

app.use('/products', routes)


const PORT = process.env.PORT || 3000 ;
app.listen(PORT, () => console.log(`App Listening on port ${PORT}!`));

module.exports = app