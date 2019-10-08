var csv = require('csv-parser')
var fs = require('fs')

var finalJson = []

fs.createReadStream('../results/clean_csv_OR.csv')
    .pipe(csv())
    .on('data', (row) => {
        makeJsonObject(row)
    })
    .on('end', () => {
        fs.writeFile('../results/clean_data_after_OR.json', JSON.stringify(finalJson), (err) => {
            if(err)
                console.log(err)
        })
    })

function makeJsonObject(row) {
    //make genres object
    var genres = [row['genre_1'], row['genre_2']]
    delete row['genre_1']
    delete row['genre_2']
    row['genres'] = genres

    //make work object
    var work = {}
    work['original_title'] = row['work_original_title']
    work['original_publication_date'] = row['work_original_publication_date']
    work['books_count'] = row['work_books_count']
    work['reviews_count'] = row['work_reviews_count']
    work['ratings_count'] = row['work_ratings_count']
    work['ratings_sum'] = row['work_ratings_sum']
    work['text_reviews_count'] = row['work_text_reviews_count']
    work['rating_dist'] = row['work_rating_dist']
    delete row['work_original_title']
    delete row['work_original_publication_date']
    delete row['work_books_count']
    delete row['work_reviews_count']
    delete row['work_ratings_count']
    delete row['work_ratings_sum']
    delete row['work_text_reviews_count']
    delete row['work_rating_dist']
    row['work'] = work

    //make authors object
    var author1 = {}
    var author2 = {}
    author1['id'] = row['author_id']
    author1['name'] = row['author_name']
    author1['gender'] = row['author_gender']
    author1['average_rating'] = row['author_average_rating']
    author1['ratings_count'] = row['author_rating_count']
    author1['image_url'] = row['author_image_url']
    author1['hometown'] = row['author_hometown']
    author1['born_at'] = row['author_born_at']
    author1['died_at'] = row['author_died_at']
    author1['works_count'] = row['author_works_count']
    author1['review_count'] = row['author_review_count']

    delete row['author_id']
    delete row['author_name']
    delete row['author_gender']
    delete row['author_average_rating']
    delete row['author_rating_count']
    delete row['author_image_url']
    delete row['author_hometown']
    delete row['author_born_at']
    delete row['author_died_at']
    delete row['author_works_count']
    delete row['author_review_count']

    author2['id'] = row['author2_id']
    author2['name'] = row['author2_name']
    author2['gender'] = row['author2_gender']
    author2['average_rating'] = row['author2_average_rating']
    author2['ratings_count'] = row['author2_rating_count']
    author2['image_url'] = row['author2_image_url']
    author2['hometown'] = row['author2_hometown']
    author2['born_at'] = row['author2_born_at']
    author2['died_at'] = row['author2_died_at']
    author2['works_count'] = row['author2_works_count']
    author2['review_count'] = row['author2_review_count']

    delete row['author2_id']
    delete row['author2_name']
    delete row['author2_gender']
    delete row['author2_average_rating']
    delete row['author2_rating_count']
    delete row['author2_image_url']
    delete row['author2_hometown']
    delete row['author2_born_at']
    delete row['author2_died_at']
    delete row['author2_works_count']
    delete row['author2_review_count']

    delete row['birthplace']
    
    var authors = []
    if(author1['id'] != '') authors.push(author1)
    if(author2['id'] != '') authors.push(author2)
    row['authors'] = authors
    // console.log(row)
    finalJson.push(row)
}
        