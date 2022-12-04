const fs = require('fs')
const express = require('express');
const cors = require('cors');
const app = express();
const path = require('path');
const sqlcon = require('./sqlcon')
const spawn = require("child_process").spawn;
var bodyParser = require('body-parser');
const multer = require('multer');
const sharp = require('sharp');

const upload = multer({
    limits: {
    fileSize: 4000000
    },
    fileFilter(req, file, cb) {
        if(!file.originalname.match(/\.(jpg|jpeg|png)$/)) {
        return cb( new Error('Please upload a valid image file'))
        }
        cb(undefined, true)
        }
    })

app.use(express.static('public'))
app.use(cors())


app.listen(8082, () => {
    console.log('Servidor express escuchando en puerto 8082');
});

app.get('/', (req, res) => {
    res.sendFile('./views/index.html',{root:__dirname})
});

app.post('/', upload.single('photo'),async (req, res) => {
    try {
            let time = Date.now(); 
            await sharp(req.file.buffer).resize({ width: 250, height: 250 , fit: 'fill'}).png().toFile(__dirname + `/uploads/${time+'-'+req.file.originalname}`)
            let path = `./uploads/${time+'-'+req.file.originalname}`;
            let alt = req.body.alt
            let breed = await getBreedName(path,alt);
            fs.unlink(path, (err) => {
                if (err) {
                  console.error(err)
                  return
                }
              });
            sqlcon.selectWhereQ(breed).then(function(results){
                res.send(results)
            });
        } catch (error) {
            console.log(error)
            res.status(400).send(error)
    }
});

app.use('/', (req,res) => {
    res.status(404).sendFile('./views/404.html',{root:__dirname})
});

async function getBreedName(path,alt) {
    return new Promise((resolve , reject) => {
        var arg2 = '';
        if(alt == 'false'){
            arg2 = 'modeloA_1.h5'
        }
        else{
            arg2 = 'modeloA_2.h5'
        }
        const childPython = spawn('./.venv/Scripts/python.exe' ,['prueba.py', path, arg2]);
        var result = '';
        childPython.stdout.on(`data` , (data) => {
            result += data.toString();
        });
        childPython.on('close' , function(code) {
            resolve(result)
        });
        childPython.on('error' , function(err){
            reject(err)
        });

    })
  };