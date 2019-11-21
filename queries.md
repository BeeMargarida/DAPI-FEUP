# Queries

1. Books about trees
    
    * **book_title:tree OR description:tree OR reviews.text:tree OR quotes:tree**

    * **(book_title:tree OR description:tree)^2.5 OR (reviews.text:tree)^1.5 OR quotes:tree**

2. Books by Leo Tolstoy
    * **authors.name:leo AND authors.name:tolstoy**

3. Books about war written after 2000
    * **(book_title:war OR description:war OR reviews.text:war OR quotes:war) AND publish_date:[2000 TO 2019]**
    * **((book_title:war OR description:war)^2.5 OR (reviews.text:war)^1.5 OR quotes:war) AND publish_date:[2000 TO 2019]**

4. Books about planting potatoes
    * **(book_title:planting AND book_title:potatoes) OR (description:planting AND description:potatoes) OR (reviews.text:planting AND reviews.text:potatoes) OR (quotes:planting AND quotes:potatoes)**
    * **(book_title:"planting potatoes"~10) OR (description:"planting potatoes"~10) OR (reviews.text:"planting potatoes"~10) OR (quotes:"planting potatoes"~10)** *// Best results* - only one book

    * **((book_title:"planting potatoes"~10) OR (description:"planting potatoes"~10))^2.5 OR (reviews.text:"planting potatoes"~10)^1.5 OR (quotes:"planting potatoes"~10)** *// same as the one with best results*

5. Books with positive reviews and language