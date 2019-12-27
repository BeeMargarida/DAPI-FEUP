import json
import csv

data_in = "../standard_dates.json"
data_out_books = "../dataset/books.csv"
data_out_genres = "../dataset/genres.csv"
data_out_works = "../dataset/works.csv"
data_out_authors = "../dataset/authors.csv"
data_out_reviews = "../dataset/reviews.csv"
data_out_quotes = "../dataset/quotes.csv"

json_file = open(data_in)
books_csv = csv.writer(open(data_out_books, "w"))
genres_csv = csv.writer(open(data_out_genres, "w"))
works_csv = csv.writer(open(data_out_works, "w"))
authors_csv = csv.writer(open(data_out_authors, "w"))
reviews_csv = csv.writer(open(data_out_reviews, "w"))
quotes_csv = csv.writer(open(data_out_quotes, "w"))

data = json.load(json_file)
books_csv.writerow(["id", "title", "description", "isbn", "publish_date", "average_rating",
                    "pages", "num_reviews", "num_ratings", "language_code", "image_url", "reviews_widget"])
genres_csv.writerow(["book_id", "name"])
works_csv.writerow(["book_id", "original_title", "original_publication_date", "books_count", "review_count", "ratings_count",
                    "ratings_sum", "text_reviews_count", "ratings_dist"])
authors_csv.writerow(["book_id", "author_id", "name", "author_ratings_count", "born_at", "died_at", "gender", "hometown",
                      "reviews_count", "works_count"])
reviews_csv.writerow(["book_id", "name", "date", "rating", "text"])
quotes_csv.writerow(["book_id", "text"])

for x in data:
    books_csv.writerow([x["book_id"],
                        x["book_title"],
                        x["description"],
                        x["isbn"],
                        x["publish_date"],
                        x["book_average_rating"],
                        x["pages"],
                        x["num_reviews"],
                        x["num_ratings"],
                        x["language_code"],
                        x["image_url"],
                        x["reviews_widget"]])

    for genre in x["genres"]:
        genres_csv.writerow([x["book_id"], genre])

    works_csv.writerow([x["book_id"],
                        x["work"]["original_title"],
                        x["work"]["original_publication_date"],
                        x["work"]["books_count"],
                        x["work"]["reviews_count"],
                        x["work"]["ratings_count"],
                        x["work"]["ratings_sum"],
                        x["work"]["text_reviews_count"],
                        x["work"]["rating_dist"]])

    for author in x["authors"]:
        authors_csv.writerow([x["book_id"],
                              author["id"],
                              author["name"],
                              author["ratings_count"],
                              author["born_at"],
                              author["died_at"],
                              author["gender"],
                              author["hometown"],
                              author["review_count"],
                              author["works_count"]])

    if "reviews" in x.keys():
        for review in x["reviews"]:
            if "rating" in review.keys():
                reviews_csv.writerow([x["book_id"],
                                    review["reviewer"],
                                    review["date"],
                                    review["rating"],
                                    review["text"]])

    if "quotes" in x.keys():
        for quote in x["quotes"]:
            quotes_csv.writerow([x["book_id"], quote])
