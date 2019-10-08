var jsonData = require('./results/data_json2900.json')
var fs = require('fs')

var result = []
var no_review = 0
var no_quote = 0

for(var i = 0; i < jsonData.length; i++){
    // if(jsonData[i]['quotes'].length === 0){
    //     no_quote++
    //     continue
    // }
    if(jsonData[i]['reviews'].length === 0){
        no_review++
        continue
    }
    if(jsonData[i]['reviews'].length !== 0)
        result.push(jsonData[i])
}


console.log("results: " + result.length)
console.log("no_review: " + no_review)
// console.log("no_quote: " + no_quote)
fs.writeFile('./results/data_json_w_rev_quo.json', JSON.stringify(result), (err) => {
    if(err)
        console.log(err)
})