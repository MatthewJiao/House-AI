const express = require('express')
const router = express.Router()
const {ensureAuthenticated} = require('../config/auth')

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

module.exports = router