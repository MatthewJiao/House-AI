const express = require('express')
const router = express.Router()
const {ensureAuthenticated} = require('../config/auth')
const fs = require('fs')
const pdfparse = require('pdf-parse')
const axios = require('axios')
const User = require('../models/User')
const puppeteer = require('puppeteer');


//router.get('/', (req, res) => res.render('welcome'))


links =[]
images = []
text = []
url = 'https://www.medicalnewstoday.com/'
router.get('/', function(req, res, next) {
   run().then(function(result){
       links = result.links;
       images = result.images;
       text = result.text;
       // console.log(links)
       // console.log(images)
       // console.log(text)
   })
   next()
}, function (req, res){
   res.render('welcome')
})

function run () {
    return new Promise(async (resolve, reject) => {
        try {
            const browser = await puppeteer.launch();
            const page = await browser.newPage();
            await page.goto(url);

            await scrollToBottom(page);
           // await page.waitFor(3000);

            let urls = await page.evaluate(() => {
                let items = document.querySelectorAll("a.css-1n50yph")

                images = new Array(items.length-1)
                 for(i = 0; i<items.length; i++){
                    images[i] = items[i].getElementsByTagName("img")[0].src
                }
                text = new Array(items.length-1)
                for(i = 0; i<items.length; i++){
                    text[i] = items[i].dataset.elementEvent
                }
                links = new Array(items.length-1)
                for(i = 0; i<items.length; i++){
                    links[i] = items[i].href
                }
                data = {
                    images, text, links
                }
                return data;
            })
            browser.close();
            return resolve(urls);
        } catch (e) {
            return reject(e);
        }
    })
}
async function scrollToBottom(page) {
    const distance = 500; // should be less than or equal to window.innerHeight
    const delay = 10;
    while (await page.evaluate(() => document.scrollingElement.scrollTop + window.innerHeight < document.scrollingElement.scrollHeight)) {
      await page.evaluate((y) => { document.scrollingElement.scrollBy(0, y); }, distance);
      await page.waitFor(delay);
    }
  }

  router.get('/dashboard', ensureAuthenticated, (req, res) =>
  res.render('dashboard', {
      name: req.user.name,
      institution: req.user.institution
  }))

 router.get('/new_patient', ensureAuthenticated, (req, res) =>
 res.render('new_patient', {
     name: req.user.name
 }))

 router.get('/news', ensureAuthenticated, (req,res) =>
 res.render('news', {
 name: req.user.name, 
 images: images,
 texts: text,
 links: links
})
)

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
     aboutMe: req.user.aboutMe,
     institution: req.user.institution

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

router.post('/send-medical',ensureAuthenticated, (req, res) => {
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

router.post('/saveProfile', ensureAuthenticated, (req, res) => {
    //console.log(req.body.pdf)
    //console.log(req.body.currentStr)
    const { name, aboutMe, institution } = req.body; 
  


      User.findOneAndUpdate(
        { email: req.user.email },
        {
          //Update database with said qualities
          $set: {
            aboutMe: aboutMe,
            name: name,
            institution: institution
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

router.post('/getUsage', ensureAuthenticated, (req, res) => {
  var sendBack = ''
  User.find({institution: req.body.institution}, function(err, data){
    let timeArray = data.map((info)=>{return info.houseUsage});
    res.send(timeArray)
  })



})

router.post('/getSymptCond', ensureAuthenticated, (req, res) => {
  User.find({institution: req.body.institution}, function(err, data){
    let mem = data.map((info)=>{return info.houseMemory});
    res.send(mem)
  })



})

router.get('/refreshDash', ensureAuthenticated, (req, res) => {
  res.render('dashboard', {
    name: req.user.name,
    institution: req.query.institution
})




})


router.post('/houseMemory', ensureAuthenticated, (req, res) => {
  //console.log(req.body.pdf)
  //console.log(req.body.currentStr)
  const { symptoms, conditions } = req.body; 
    var current = req.user.houseMemory
    var newMem = current.concat([symptoms])   
    newMem = newMem.concat([conditions])
    var seconds = new Date().getTime() / 1000;
    newMem = newMem.concat([[Date(), seconds]])
    var current2 = req.user.houseUsage
    current2 = current2.concat([seconds])

    User.findOneAndUpdate(
      { email: req.user.email },
      {
        //Update database with said qualities
        $set: {
          houseMemory: newMem,
          houseUsage: current2
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

router.post('/getMemory', ensureAuthenticated, (req, res) => {

    
    res.send(req.user.houseMemory)
})

module.exports = router