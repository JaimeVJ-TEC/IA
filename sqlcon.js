const { query } = require('express');
const mysql = require('mysql');

function getCon(){
    var con = mysql.createConnection({
        host : '127.0.0.1',
        user : 'root',
        database : 'dogbreeds',
    })
    return con;
}

function selectWhereQ(nombre){
    con = getCon();
    con.connect();
    nombre = nombre.trim();
    return new Promise(function(resolve,reject){
        let query = "SELECT nombre,descripcion FROM razas where nombre = ?"
        con.query(query,[nombre], function(error, results) {
            if(results == undefined){
                reject(new Error("Undefined result"))
            } else {
                resolve(results)
            }
        })
    });
}

exports.getCon = getCon;
exports.selectWhereQ = selectWhereQ;