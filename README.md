# Goodreads Search Engine

## Setup

1. Create a virtual environment with `python -m venv venv`
2. Activate the virtualenv with `. venv/bin/activate`
3. Enter the scripts directory with `cd scripts/`
4. Install dependencies with `pip install -r requirements.txt`

### Useful Tools & Links

- https://github.com/iiimosley/GoodQuotes
- https://github.com/sefakilic/goodreads
- https://pypi.org/project/goodreads-api-client/ (maybe use this one to get complete json)
- https://isbndb.com/apidocs#/Book/get_book__isbn_ (amazing book database - but is paid)
- https://www.goodreads.com/topic/show/159957-get-quotes-api-method


## Solr

To run solr:

- sudo systemctl start solr
- cd /opt/solr
- sudo -u solr bin/solr create_core -c dapi (create core, only first time)
- sudo -u solr bin/post -c dapi <path_to_json>.json (add data to core, only first time)
