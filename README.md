neotext
===============

An api server that:
  * accepts quote POST requests from the client, of the form:
     * url
     * quote
  * looks up the cited URL's html
  * calculates the context surrounding the quote
  * saves the contextual data to a Postgres database
  * uploads the quote-context json file to Amazon S3.

## Setup ##
  * Make sure you have Python 3.4 or higher
  * Clone the Git Repository:
    - git clone https://github.com/neotext/neotext-django-server.git
  * Setup Virtual Environment:
      1. pip install virtualenv
      2. virtualenv venv
      3. source venv/bin/activate
  * In main folder containing requirements.txt:
      - pip install -r requirements.txt
  * add your own neotext folder to the python path
	 - export PYTHONPATH="$PYTHONPATH:/home/timlangeman/webapps/neotext/neotext"
    [view python path](http://stackoverflow.com/questions/1489599/how-do-i-find-out-my-python-path-using-python)
  * Create Postgres Database:
    - python manage.py syncdb

## Dependencies ##
  * Python 3.4,
  * Django 1.8,
  * Postgres
  * [django-cors-headers](https://github.com/ottoyiu/django-cors-headers/)
  * [psycopg2](http://initd.org/psycopg/)
  * [bs4](https://www.crummy.com/software/BeautifulSoup/)
  * [gevent](http://www.gevent.org/)
  * [tinys3](https://www.smore.com/labs/tinys3/)
  * [django_extensions](https://github.com/django-extensions/django-extensions)

## Changelog ##

v0.01 - initial release

## Credits ##

Be the first contributor.  Your name here!
