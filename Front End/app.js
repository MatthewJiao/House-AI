const express = require('express')
const expressLayouts = require('express-ejs-layouts')
const mongoose = require('mongoose')
const flash = require('connect-flash')
const session = require('express-session')
const passport = require('passport')
var bodyParser = require('body-parser')


const app = express()


//app.use(bodyParser.urlencoded({ extended: false }))
//app.use(bodyParser.json())


require('./config/passport')(passport)

const db = require('./config/keys').MongoURI
mongoose.connect(db, {useNewUrlParser: true, useUnifiedTopology: true})
.then(() => console.log('mongo db connected...'))
.catch(err => console.log(err))

app.use(expressLayouts)
app.set('view engine', 'ejs')

app.use(express.static(__dirname + '/public'));

app.use(express.json({limit: '50mb'}));

app.use(express.urlencoded({extended: false, limit: '50mb'}))

app.use(session({
    secret: 'secret',
    resave: true,
    saveUninitialized: true,
  }))

app.use(passport.initialize());
app.use(passport.session());

app.use(flash())

app.use((req, res, next) => {
    res.locals.success_msg = req.flash('success_msg')
    res.locals.error_msg = req.flash('error_msg')
    res.locals.error = req.flash('error')

    next()
})

//routes
app.use('/', require('./routes/index'))
app.use('/users', require('./routes/users'))


const PORT = process.env.PORT || 5000

app.listen(PORT, console.log(`server started on port ${PORT}`))