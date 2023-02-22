const request = require('supertest')
const app  = require('../Server/server')


describe('Sample Test', () => {
    it('should test that true === true', () => {
      expect(true).toBe(true)
    })
  })

describe('Get Products', () => {
  it('should get products', async () => {
    const res = await request(app)
      .get('/products')
    expect(res.statusCode).toEqual(200)

  })
})

describe('Get Products by id', () => {
    it('should get products by specific id', async () => {
      const res = await request(app)
        .get('/products/1234')
      expect(res.statusCode).toEqual(200)
    })
  })

  describe('Get Products style by id', () => {
    it('should get product styles by id', async () => {
      const res = await request(app)
        .get('/products/12344/styles')
      expect(res.statusCode).toEqual(200)
    })
  })

  describe('Get Products related by id', () => {
    it('should get products related by id', async () => {
      const res = await request(app)
        .get('/products/12344/related')
      expect(res.statusCode).toEqual(200)
    })
  })