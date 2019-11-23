# Queries

1. **Books about war**
    
    * book_title:war OR description:war OR reviews.text:war OR quotes:war

    * (book_title:war OR description:war)^2.5 OR (reviews.text:war)^1.5 OR quotes:war

2. **Books by Leo Tolstoy**
    * authors.name:leo AND authors.name:tolstoy

3. **Books about war written after 2000**
    * (book_title:war OR description:war OR reviews.text:war OR quotes:war) AND publish_date:[2000 TO 2019]
    * ((book_title:war OR description:war)^2.5 OR (reviews.text:war)^1.5 OR quotes:war) AND publish_date:[2000 TO 2019]

4. **History books about world war**
    * (book_title:world AND book_title:war) OR (description:world AND description:war) OR (reviews.text:world AND reviews.text:war) OR (quotes:world AND quotes:war)
    * ((book_title:"world war 2"~10) OR (description:"world war"~10) OR (reviews.text:"world war"~10) OR (quotes:"world war"~10)) AND genres:history *// Best results* - only one book

    * (((book_title:"world war"~10) OR (description:"world war"~10))^2.5 OR (reviews.text:"world war"~10)^1.5 OR (quotes:"world war"~10)) AND genres:history *// same as the one with best results*

5. **Books with positive reviews (score and language)** - TODO: IMPROVE SYNONYMS
    * reviews.text:good AND reviews.text:love AND reviews.rating:[4 TO 5]

6. **Books about love by a good rated author** -- TODO: IMPROVE SYNONYMS
    * (book_title:love OR description:love OR reviews.text:love OR quotes:love) AND genres:romance with SORT authors.average_rating DESC
    * (book_title:love OR description:love OR reviews.text:love OR quotes:love) AND (genres:romance)^1.5 with SORT authors.average_rating DESC

7. **Best rated movies about depression**
    * book_title:depression OR description:depression OR reviews.text:depression OR quotes:depression with SORT book_average_rating DESC

8. **Books about the world war II with positive reviews and good rating**
    * ((book_title:"world war 2"~5 OR book_title:"world war II"~5) OR (description:"world war 2"~5 OR description:"world war II"~5) OR (reviews.text:"world war 2"~5 OR reviews.text:"world war II"~5) OR (quotes:"world war 2"~5 OR quotes:"world war II"~5)) AND (reviews.text:good OR reviews.text:"best book" OR reviews.text:love) AND book_average_rating:[4.5 TO 5]

9. **Books about football with positive reviews and good rating**
    * ((book_title:football) OR (description:football) OR (reviews.text:football) OR (quotes:football)) AND (reviews.text:good OR reviews.text:"best book" OR reviews.text:love) AND book_average_rating:[4 TO 5]

    * (((book_title:football) OR (description:football))^2.5 OR (reviews.text:football)^1.5 OR (quotes:football)) AND (reviews.text:good OR reviews.text:"best book" OR reviews.text:love) AND book_average_rating:[4 TO 5]

10. **Book by an author, which reviews mention George RR Martin**
    * reviews.text:"George RR Martin*~10

# Evaluation

1. **Books about war**
    * **S1**: Precision = 10/10 = 1
    * **S2**: Precision = 10/10 = 1

    * **S1**: MAP = 1/10*(10) = 1
    * **S2**: MAP = 1/10*(10) = 1

4. **History books about world war**
    * **S1**: Precision = 8/10 = 0.8
    * **S2**: Precision = 8/10 = 0.8

    * **S1**: MAP = 1/8*(1 + 1 + 1 + 4/5 + 5/6 + 6/7 + 7/8 + 8/10) = 7.165/8 = 0.896
    * **S2**: MAP = 1/8*(1 + 1 + 1 + 4/5 + 5/6 + 6/7 + 7/8 + 8/10) = 7.165/8 = 0.896

10. **Book by an author, which reviews mention George RR Martin**
    * **S1**: Precision = 10/10 = 1

    * **S1**: MAP = 1/10*10 = 1

9. **Books about football with positive reviews and good rating**
    * **S1**: Precision = 6/10 = 0.6
    * **S2**: Precision = 6/10 = 0.6

    * **S1**: MAP = 1/6*(1 + 1 + 1 + 4/7 + 5/8 + 6/9) = 4.863/6 = 0.811
    * **S2**: MAP = 1/6*(1 + 1 + 1 + 4/6 + 5/7 + 6/9) = 5.0476/6 = 0.841

## Setup
Copy the file synonyms.txt into /opt/solr/server/solr/dapi/conf