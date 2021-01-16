const express = require('express')
const router = express.Router()
const {ensureAuthenticated} = require('../config/auth')

router.get('/', (req, res) => res.render('welcome'))
router.get('/dashboard', ensureAuthenticated, (req, res) =>
 res.render('dashboard', {
     name: req.user.name
 }))

 router.get('/icons', ensureAuthenticated, (req, res) =>
 res.render('icons', {
     name: req.user.name
 }))

 router.get('/map', ensureAuthenticated, (req, res) =>
 res.render('map', {
     name: req.user.name
 }))

 router.get('/notifications', ensureAuthenticated, (req, res) =>
 res.render('notifications', {
     name: req.user.name
 }))

 router.get('/user', ensureAuthenticated, (req, res) =>
 res.render('user', {
     name: req.user.name
 }))

 router.get('/tables', ensureAuthenticated, (req, res) =>
 res.render('tables', {
     name: req.user.name
 }))

 router.get('/typography', ensureAuthenticated, (req, res) =>
 res.render('typography', {
     name: req.user.name
 }))

 router.get('/rtl', ensureAuthenticated, (req, res) =>
 res.render('rtl', {
     name: req.user.name
 }))

module.exports = router