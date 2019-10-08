import goodreads_api_client as gr
import pandas as pd
import sys
from bs4 import BeautifulSoup


api_key = 'UHAS2y3w3m61D2eC0xGwg'
api_secret = 'Oy8yu9oz5Z30vwncybi03WZsB9fk5yYbj10Stem8o'
data_in = "../datasets/wd2000_after_OR.csv"
data_out = "results/partial_csv_OR.csv"
bookID_row = 8
index = 0


# client = gr.Client(developer_key=api_key, developer_secret=api_secret)
client = gr.Client(developer_key=api_key)

csv_doc = pd.read_csv(data_in)
new_columns = ['isbn', 'image_url', 'publisher', 'language_code', 'description', 'author_image_url', 'author_hometown', 'author_born_at',
               'author_died_at', 'author_works_count', 'author2_average_rating', 'author2_gender', 'author2_id', 'author2_name', 'author2_rating_count', 'author2_review_count', 'author2_image_url', 'author2_hometown', 'author2_born_at', 'author2_died_at', 'author2_works_count',
               'work_books_count', 'work_reviews_count', 'work_ratings_sum', 'work_ratings_count', 'work_text_reviews_count', 'work_original_publication_date', 'work_original_title', 'work_rating_dist']

for column_name in new_columns:
    csv_doc[column_name] = ""

for index, row in csv_doc.iterrows():
    print(row[bookID_row])
    print(index)

    # Get info of the book
    try:
        book = client.Book.show(row[bookID_row])  # 1128434 - 2832909
    except Exception:
        continue

    keys_wanted = ['isbn', 'image_url', 'publisher', 'language_code',
                   'description', 'authors', 'reviews_widget', 'work']
    reduced_book = {k: v for k, v in book.items() if k in keys_wanted}
    #book_json = json.loads(json.dumps(reduced_book))

    # Add to csv all the extra fields
    csv_doc.at[index, 'isbn'] = reduced_book["isbn"]
    csv_doc.at[index, 'image_url'] = reduced_book["image_url"]
    csv_doc.at[index, 'publisher'] = reduced_book["publisher"]
    csv_doc.at[index, 'language_code'] = reduced_book["language_code"]
    csv_doc.at[index, 'description'] = reduced_book["description"]
    csv_doc.at[index, 'work_books_count'] = reduced_book["work"]["books_count"]["#text"]
    csv_doc.at[index, 'work_reviews_count'] = reduced_book["work"]["reviews_count"]["#text"]
    csv_doc.at[index, 'work_ratings_sum'] = reduced_book["work"]["ratings_sum"]["#text"]
    csv_doc.at[index, 'work_ratings_count'] = reduced_book["work"]["ratings_count"]["#text"]
    csv_doc.at[index, 'work_text_reviews_count'] = reduced_book["work"]["text_reviews_count"]["#text"]
    csv_doc.at[index, 'work_original_title'] = reduced_book["work"]["original_title"]
    csv_doc.at[index, 'work_rating_dist'] = reduced_book["work"]["rating_dist"]

    # Original publication date
    if (not "#text" in reduced_book["work"]["original_publication_month"].keys() or not "#text" in reduced_book["work"]["original_publication_day"].keys()) and "#text" in reduced_book["work"]["original_publication_year"].keys():
        csv_doc.at[index, 'work_original_publication_date'] = reduced_book["work"]["original_publication_year"]["#text"]
    elif "#text" in reduced_book["work"]["original_publication_year"].keys():
        csv_doc.at[index, 'work_original_publication_date'] = reduced_book["work"]["original_publication_day"]["#text"] + "/" + \
            reduced_book["work"]["original_publication_month"]["#text"] + \
            "/" + reduced_book["work"]["original_publication_year"]["#text"]

    # Get reviews URL
    parsed_html = BeautifulSoup(reduced_book["reviews_widget"], 'html.parser')
    reviews_url = parsed_html.iframe.get('src')
    csv_doc.at[index, 'reviews_widget'] = reviews_url

    # Get authors info
    authors = reduced_book["authors"]["author"]
    index_author = 1
    if len(authors) > 1 and isinstance(authors, list):
        for idx, author in enumerate(authors):
            if author["role"] == None and author["role"] != "Translator":
                # Make API Request to get info of author
                try:
                    author_info = client.Author.show(author["id"])
                    print(author['name'])

                    if index_author == 1:
                        csv_doc.at[index,
                                   'author_average_rating'] = author["average_rating"]
                        csv_doc.at[index,
                                   'author_gender'] = author_info["gender"]
                        csv_doc.at[index, 'author_id'] = author["id"]
                        csv_doc.at[index, 'author_name'] = author["name"]
                        csv_doc.at[index,
                                   'author_rating_count'] = author["ratings_count"]
                        csv_doc.at[index,
                                   'author_review_count'] = author["text_reviews_count"]
                        csv_doc.at[index, 'author_id'] = author["id"]
                        csv_doc.at[index,
                                   'author_image_url'] = author["image_url"]["#text"]
                        csv_doc.at[index,
                                   'author_hometown'] = author_info["hometown"]
                        csv_doc.at[index,
                                   'author_born_at'] = author_info["born_at"]
                        csv_doc.at[index,
                                   'author_died_at'] = author_info["died_at"]
                        csv_doc.at[index,
                                   'author_works_count'] = author_info["works_count"]
                    elif index_author == 2:
                        csv_doc.at[index,
                                   'author2_average_rating'] = author["average_rating"]
                        csv_doc.at[index,
                                   'author2_gender'] = author_info["gender"]
                        csv_doc.at[index, 'author2_id'] = author["id"]
                        csv_doc.at[index, 'author2_name'] = author["name"]
                        csv_doc.at[index,
                                   'author2_rating_count'] = author["ratings_count"]
                        csv_doc.at[index,
                                   'author2_review_count'] = author["text_reviews_count"]
                        csv_doc.at[index, 'author2_id'] = author["id"]
                        csv_doc.at[index,
                                   'author2_image_url'] = author["image_url"]["#text"]
                        csv_doc.at[index,
                                   'author2_hometown'] = author_info["hometown"]
                        csv_doc.at[index,
                                   'author2_born_at'] = author_info["born_at"]
                        csv_doc.at[index,
                                   'author2_died_at'] = author_info["died_at"]
                        csv_doc.at[index,
                                   'author2_works_count'] = author_info["works_count"]
                    else:
                        continue

                    index_author = index_author + 1
                except Exception as e:
                    print("\n\nEXCEPTION\n\n")
                    print(e)
                    continue
    else:
        if authors["role"] == None and authors["role"] != "Translator":
            # Make API Request to get info of author
            try:
                author_info = client.Author.show(authors["id"])
                print(authors['name'])
                csv_doc.at[index,
                           'author_average_rating'] = authors["average_rating"]
                csv_doc.at[index, 'author_gender'] = author_info["gender"]
                csv_doc.at[index, 'author_id'] = authors["id"]
                csv_doc.at[index, 'author_name'] = authors["name"]
                csv_doc.at[index,
                           'author_rating_count'] = authors["ratings_count"]
                csv_doc.at[index,
                           'author_review_count'] = authors["text_reviews_count"]
                csv_doc.at[index, 'author_id'] = authors["id"]
                csv_doc.at[index,
                           'author_image_url'] = authors["image_url"]["#text"]
                csv_doc.at[index, 'author_hometown'] = author_info["hometown"]
                csv_doc.at[index, 'author_born_at'] = author_info["born_at"]
                csv_doc.at[index, 'author_died_at'] = author_info["died_at"]
                csv_doc.at[index,
                           'author_works_count'] = author_info["works_count"]
            except Exception:
                continue

csv_doc.to_csv(data_out, index=False)

# Get info on the author
#     authors = book_json["authors"]["author"]
#     if len(authors) > 1 and isinstance(authors, list):
#         for idx, author in enumerate(authors):
#             if author["role"] == None:
#                 # Make API Request to get info of author
#                 try:
#                     author_info = client.Author.show(author["id"])
#                     print(author['name'])
#                     author = author['name']
#                     book_json["authors"]["author"][idx]["hometown"] = author_info['hometown']
#                     book_json["authors"]["author"][idx]["born_at"] = author_info['born_at']
#                     book_json["authors"]["author"][idx]["died_at"] = author_info['died_at']
#                     book_json["authors"]["author"][idx]["gender"] = author_info['gender']
#                     book_json["authors"]["author"][idx]["works_count"] = author_info['works_count']
#                 except Exception:
#                     continue
#             elif author["role"] == 'Translator':
#                 del book_json["authors"]["author"][idx]
#     else:
#         if authors["role"] == None:
#             # Make API Request to get info of author
#             try:
#                 author_info = client.Author.show(authors["id"])
#                 print(authors['name'])
#                 author = authors['name']
#                 book_json["authors"]["author"]["hometown"] = author_info['hometown']
#                 book_json["authors"]["author"]["born_at"] = author_info['born_at']
#                 book_json["authors"]["author"]["died_at"] = author_info['died_at']
#                 book_json["authors"]["author"]["gender"] = author_info['gender']
#                 book_json["authors"]["author"]["works_count"] = author_info['works_count']
#             except Exception:
#                 continue
#     # Add genres - rows 14 and 15
#     if(row[14] == row[15]):
#         book_json["genres"] = [row[14]]
#     else:
#         book_json["genres"] = [row[14], row[15]]

#     # Get quotes
#     regex = re.compile(".*?\((.*?)\)")
#     book_title = re.sub("[\(\[].*?[\)\]]", "", book_json["title"])
#     print(book_title)

#     data = get_quotes(book_title, None)

#     quotes = []

#     if(data and "quotes" in data):
#         print("quotes")
#         # Parse through quotes and get the ones related to the book and author
#         quotes += get_valid_quotes(data["quotes"], author, book_title)

#         # Get more 4 pages of quotes and do the same of the above
#         pages = 1
#         total_pages = data["total_pages"]
#         while (pages < 4 and total_pages > 4):
#             data = get_quotes(book_title, pages)

#             if(data):
#                 quotes += get_valid_quotes(data["quotes"],
#                                             author, book_title)
#             pages = pages + 1

#     # Append quotes to the json
#     book_json["quotes"] = quotes

#     # Get reviews
#     parsed_html = BeautifulSoup(book_json["reviews_widget"], 'html.parser')
#     reviews_url = parsed_html.iframe.get('src')
#     try:
#         r = requests.get(url=reviews_scrapper_url,
#                             params={'url': reviews_url})
#         if(r.status_code == 500):
#             continue
#         data = r.json()
#         book_json["reviews"] = data
#     except Exception:
#         continue

#     # Add book to json of books
#     books.append(book_json)

#     if index % 100 == 0:
#         with open(data_out + str(index) + ".json", 'w', newline='') as out_file_temp:
#             json.dump(books, out_file_temp)

#     index = index + 1

# json.dump(books, out_file)
