const express = require('express')
const router = express.Router()
const {ensureAuthenticated} = require('../config/auth')
const fs = require('fs')
const pdfparse = require('pdf-parse')
const axios = require('axios')



router.get('/', (req, res) => res.render('welcome'))
router.get('/dashboard', ensureAuthenticated, (req, res) =>
 res.render('dashboard', {
     name: req.user.name
 }))

 router.get('/new_patient', ensureAuthenticated, (req, res) =>
 res.render('new_patient', {
     name: req.user.name
 }))

 router.get('/news', ensureAuthenticated, (req, res) =>
 res.render('news', {
     name: req.user.name
 }))

 router.get('/memory', ensureAuthenticated, (req, res) =>
 res.render('memory', {
     name: req.user.name
 }))

 router.get('/user', ensureAuthenticated, (req, res) =>
 res.render('user', {
     name: req.user.name
 }))

//  router.get('/tables', ensureAuthenticated, (req, res) =>
//  res.render('tables', {
//      name: req.user.name
//  }))

//  router.get('/typography', ensureAuthenticated, (req, res) =>
//  res.render('typography', {
//      name: req.user.name
//  }))

//  router.get('/rtl', ensureAuthenticated, (req, res) =>
//  res.render('rtl', {
//      name: req.user.name
//  }))

//router.post('/send-medical', (req, res) => {
    //const {name, email, password, password2, registeredID} = req.body
    /*
    console.log('test')
    const {myFile} = req.body
    const path = [req.body,'sampleFiles/sample.pdf']
    const com = path.join('')
    //console.log('tesint', com)
    const pdffile = fs.readFileSync(com)

    pdfparse(pdffile).then(function (data) {
        console.log(data.numpages)
    })

    //console.log(myFile.files)

*/
//})

router.post('/send-medical', (req, res) => {
    //console.log(req.body.pdf)
    //console.log(req.body.currentStr)
    
    var input = req.body.pdf.concat(req.body.separator.concat(req.body.currentStr))
    //console.log(input)
    var urlID = "http://127.0.0.1:5000/predict/".concat(input)
    //console.log(urlID)
    axios({
        method: "GET",
        withCredentials: true,
        url: urlID
      }).then((te) => res.send(te.data))
    
})


module.exports = router