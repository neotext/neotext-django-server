Neotext
===============

An API server that computes the context surrounding quotations on a submitted URL.
  * accepts quote POST requests from the client, of the form:
     * url
     * quote
  * looks up the cited URL's html
  * calculates the context surrounding the quote
  * saves the contextual data to a Postgres database
  * uploads the quote-context json file to Amazon S3.

## Setup ##
  * Python 3.4 or higher is required
  * Clone the Git Repository:
    - git clone https://github.com/neotext/neotext-django-server.git
  * Setup Virtual Environment:
      1. pip install virtualenv
      2. virtualenv venv
      3. source venv/bin/activate
  * In main folder containing requirements.txt:
      - pip install -r requirements.txt
  * Add your own neotext folder to the python path
	 - export PYTHONPATH="$PYTHONPATH:/home/timlangeman/webapps/neotext/neotext"
   - [view python path](http://stackoverflow.com/questions/1489599/how-do-i-find-out-my-python-path-using-python)
  * Setup your own Database & AWS Credentials in settings.py
  * Create Postgres Database:
    - python manage.py syncdb


## Dependencies ##
  * [Python](https://www.python.org/) 3.4,
  * [Postgres](https://www.postgresql.org/)
  * [django](https://www.djangoproject.com/),
  * [psycopg2](http://initd.org/psycopg/)
  * [bs4](https://www.crummy.com/software/BeautifulSoup/)
  * [tinys3](https://www.smore.com/labs/tinys3/)
  * [gevent](http://www.gevent.org/)
  * [django-cors-headers](https://github.com/ottoyiu/django-cors-headers/)  
  * [django_extensions](https://github.com/django-extensions/django-extensions)

## Changelog ##

v0.01 - initial release

## Credits ##
Created by Tim Langeman.  Inspired by Ted Nelson.

Be the first contributor.  Your name here!
