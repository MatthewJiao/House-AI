const mongoose = require('mongoose')

const UserSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true
    },
    medicalID: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    aboutMe: {
        type: String,
        required: false,
    },
    houseMemory: {
        type: [[String]],
        default: []
    },
    houseUsage: {
        type: [Number],
        default: []
    },
    institution: {
        type: String,
        required: true
    },
    date: {
        type: Date,
        default: Date.now
    },
})

const User = mongoose.model('User', UserSchema)
module.exports = User