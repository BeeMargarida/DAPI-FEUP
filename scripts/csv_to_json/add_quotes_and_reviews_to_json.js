var fs = require('fs')
// var jsonWRQ = require('../results/data_json_w_rev_quo.json')
var jsonWData = require('../results/clean_data_after_OR.json')
var jsonWRQ = require('../results/dict.json')

/* isto é só para criar um ficheiro com um map do json com as reviews e quotes, para dar para aceder a um book logo pelo book_id, em vez de ter de percorrer o array todo
var dict = {}

for(var i = 0; i < jsonWRQ.length; i++){
    dict[jsonWRQ[i]['id']] = jsonWRQ[i]
}

fs.writeFile('../results/dict.json', JSON.stringify(dict), (err) => {
    if(err)
    console.log(err)
})*/

var booksNotInDS = []

for(let book of jsonWData) {
    if(book['book_id'] == null || book['book_id'] == '')
        console.log("Empty id: " + book)

    if(jsonWRQ[book['book_id']] == null){
        booksNotInDS.push(book['book_id'])
        continue
    }
    book['reviews'] = jsonWRQ[book['book_id']]['reviews']
    book['quotes'] = jsonWRQ[book['book_id']]['quotes']
}

for(let b of booksNotInDS)
    console.log(b)

console.log(booksNotInDS.length)

fs.writeFile('../results/final_json_w_quotes_reviews.json', JSON.stringify(jsonWData), (err) => {
    if(err)
    console.log(err)
})