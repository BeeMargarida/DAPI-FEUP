import goodreads_api_client as gr
import json
import csv
import sys
from collections import OrderedDict
import requests
import re
from bs4 import BeautifulSoup

api_key = 'UHAS2y3w3m61D2eC0xGwg'
api_secret = 'Oy8yu9oz5Z30vwncybi03WZsB9fk5yYbj10Stem8o'
data_in = "../datasets/working_dataset_3000.csv"
data_out = "results/data_json"
# "https://goodquotesapi.herokuapp.com/title/"
quotes_url = "http://localhost:8080/title/"
reviews_scrapper_url = "http://localhost:5050/"
bookID_row = 12
index = 0


def check_quote_valid(quote, author, book_title):
    return quote["author"] == author and quote["publication"] == book_title


def get_quotes(book_title, pages):
    if(pages):
        url = quotes_url + \
            book_title.replace(" ", "+") + "?page=" + str(pages)
    else:
        url = quotes_url + book_title.replace(" ", "+")

    try:
        r = requests.get(url=url)
        if(r.status_code == 500):
            return None
        else:
            data = r.json()
            return data
    except Exception:
        return None


def get_valid_quotes(quotes, author, book_title):
    final_quotes = []
    for quote in quotes:
        if check_quote_valid(quote, author, book_title):
            final_quotes.append(quote["quote"])
    return final_quotes


# client = gr.Client(developer_key=api_key, developer_secret=api_secret)
client = gr.Client(developer_key=api_key)
books = []

with open(data_in, 'r', newline='') as in_file, open(data_out + ".json", 'w', newline='') as out_file:
    reader = csv.reader(in_file)
    row0 = next(reader)

    for row in reader:
        print(row[bookID_row])
        print(index)

        # Get info of the book
        try:
            book = client.Book.show(row[bookID_row])  # 1128434 - 2832909
        except Exception:
            continue

        keys_wanted = ['id', 'title', 'isbn', 'image_url', 'publication_year', 'publication_month', 'publication_day', 'publisher',
                       'language_code', 'description', 'work', 'average_rating', 'num_pages', 'ratings_count', 'text_reviews_count', 'authors', 'popular_shelves', 'reviews_widget']
        reduced_book = {k: v for k, v in book.items() if k in keys_wanted}
        book_json = json.loads(json.dumps(reduced_book))

        # Get info on the author
        authors = book_json["authors"]["author"]
        if len(authors) > 1 and isinstance(authors, list):
            for idx, author in enumerate(authors):
                if author["role"] == None:
                    # Make API Request to get info of author
                    try:
                        author_info = client.Author.show(author["id"])
                        print(author['name'])
                        author = author['name']
                        book_json["authors"]["author"][idx]["hometown"] = author_info['hometown']
                        book_json["authors"]["author"][idx]["born_at"] = author_info['born_at']
                        book_json["authors"]["author"][idx]["died_at"] = author_info['died_at']
                        book_json["authors"]["author"][idx]["gender"] = author_info['gender']
                        book_json["authors"]["author"][idx]["works_count"] = author_info['works_count']
                    except Exception:
                        continue
                elif author["role"] == 'Translator':
                    del book_json["authors"]["author"][idx]
        else:
            if authors["role"] == None:
                # Make API Request to get info of author
                try:
                    author_info = client.Author.show(authors["id"])
                    print(authors['name'])
                    author = authors['name']
                    book_json["authors"]["author"]["hometown"] = author_info['hometown']
                    book_json["authors"]["author"]["born_at"] = author_info['born_at']
                    book_json["authors"]["author"]["died_at"] = author_info['died_at']
                    book_json["authors"]["author"]["gender"] = author_info['gender']
                    book_json["authors"]["author"]["works_count"] = author_info['works_count']
                except Exception:
                    continue
        # Add genres - rows 14 and 15
        if(row[14] == row[15]):
            book_json["genres"] = [row[14]]
        else:
            book_json["genres"] = [row[14], row[15]]

        # Get quotes
        regex = re.compile(".*?\((.*?)\)")
        book_title = re.sub("[\(\[].*?[\)\]]", "", book_json["title"])
        print(book_title)

        data = get_quotes(book_title, None)

        quotes = []

        if(data and "quotes" in data):
            print("quotes")
            # Parse through quotes and get the ones related to the book and author
            quotes += get_valid_quotes(data["quotes"], author, book_title)

            # Get more 4 pages of quotes and do the same of the above
            pages = 1
            total_pages = data["total_pages"]
            while (pages < 4 and total_pages > 4):
                data = get_quotes(book_title, pages)

                if(data):
                    quotes += get_valid_quotes(data["quotes"],
                                               author, book_title)
                pages = pages + 1

        # Append quotes to the json
        book_json["quotes"] = quotes

        # Get reviews
        parsed_html = BeautifulSoup(book_json["reviews_widget"], 'html.parser')
        reviews_url = parsed_html.iframe.get('src')
        try:
            r = requests.get(url=reviews_scrapper_url,
                             params={'url': reviews_url})
            if(r.status_code == 500):
                continue
            data = r.json()
            book_json["reviews"] = data
        except Exception:
            continue

        # Add book to json of books
        books.append(book_json)

        if index % 100 == 0:
            with open(data_out + str(index) + ".json", 'w', newline='') as out_file_temp:
                json.dump(books, out_file_temp)

        index = index + 1

    json.dump(books, out_file)
