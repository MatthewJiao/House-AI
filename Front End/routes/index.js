const express = require('express')
const router = express.Router()
const {ensureAuthenticated} = require('../config/auth')
const fs = require('fs')
const pdfparse = require('pdf-parse')
const axios = require('axios')
const User = require('../models/User')



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
     name: req.user.name }))

 router.get('/memory', ensureAuthenticated, (req, res) =>
 res.render('memory', {
     name: req.user.name
 }))

 router.get('/user', ensureAuthenticated, (req, res) => {
    //console.log(req.user.aboutMe)

 res.render('user', {
     name: req.user.name,
     email: req.user.email,
     firstName: req.user.name.split(" ")[0],
     lastName: req.user.name.split(" ")[1],
     medicalID: req.user.medicalID,
     aboutMe: req.user.aboutMe
 })})

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

router.post('/saveProfile', (req, res) => {
    //console.log(req.body.pdf)
    //console.log(req.body.currentStr)
    const { name, aboutMe } = req.body; 
  


      User.findOneAndUpdate(
        { email: req.user.email },
        {
          //Update database with said qualities
          $set: {
            aboutMe: aboutMe,
            name: name
          },
        },
        { new: true },
        (err, result) => {
          if (err) {
            console.log(err);
          }
          //console.log(result);
        }
      );
    
})


router.post('/houseMemory', (req, res) => {
  //console.log(req.body.pdf)
  //console.log(req.body.currentStr)
  const { symptoms, conditions } = req.body; 
    var current = req.user.houseMemory
    var newMem = current.concat([symptoms])   
    newMem = newMem.concat([conditions])
    newMem = newMem.concat(Date())
    User.findOneAndUpdate(
      { email: req.user.email },
      {
        //Update database with said qualities
        $set: {
          houseMemory: newMem
        },
      },
      { new: true },
      (err, result) => {
        if (err) {
          console.log(err);
        }
       // console.log(result);
      }
    );
  
})

router.post('/getMemory', (req, res) => {

    
    res.send(req.user.houseMemory)
})

module.exports = router