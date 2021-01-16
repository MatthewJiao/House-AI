const express = require('express')
const router = express.Router()
const bcrypt = require('bcryptjs')
const passport = require('passport')
const User = require('../models/User')

router.get('/login', (req, res) => res.render('login'))

router.get('/register', (req, res) => res.render('register'))

router.post('/register', (req, res) => {
    const {name, email, password, password2, registeredID} = req.body
    let errors = []
    let whitelist = ['1111','2222']

    if(!name || !email || !password || !password2){
        errors.push({msg: 'Please fill in all fields'})
    }

    if(password !== password2){
        errors.push({msg: 'Passwords do not match'})
    }

    if(password.length < 6) {
        errors.push({msg: 'Password should be at least 6 characters'})
    }

    if(!whitelist.includes(registeredID)){
        errors.push({msg: 'Medical ID must be valid'})
    }

    if(errors.length > 0){
        res.render('register', {errors, name, email, password, password2, registeredID})
    } else {
        User.findOne({email: email})
        .then(user => {
            if(user){
                errors.push({msg: 'Email is already registered'})
                res.render('register', {errors, name, email, password, password2, registeredID})
            } else {
                const newUser = new User({
                    name,
                    email,
                    password,
                    medicalID: registeredID,
                    aboutMe: "Knock, knock! Who’s there? Colin who? Colin the doctor… I’m sick!"
                })
                bcrypt.genSalt(10, (err, salt) => bcrypt.hash(newUser.password, salt, (err, hash) => {
                    if(err) throw err

                    newUser.password = hash
                    newUser.save()
                    .then(user => {
                        req.flash('success_msg', 'You are now registered')
                        res.redirect('/users/login')
                    })
                    .catch(err => console.log(err))
                }))

            }
        })
    }


})

router.post('/login', (req, res, next) => {
    passport.authenticate('local', {
        successRedirect: '/dashboard',
        failureRedirect: '/users/login',
        failureFlash: true
    })(req, res, next)
})

router.get('/logout', (req, res) => {
    req.logout()
    req.flash('success_msg', 'You are logged out')
    res.redirect('/users/login')
})

module.exports = router