neotext-server
===============

An api server that:
  * accepts quote POST requests from the client, of the form:
     * url
     * quote
  * looks up the cited URL's html
  * calculates the context surrounding the quote 
  * saves the contextual data to a database
  * saves the quote-context in json form to Amazon S3. (future)
  * returns quote-context in json form

## Setup ##
  * setup python and [django](https://docs.djangoproject.com/en/1.8/topics/install/)
  * add neotext folder to the python path
	export PYTHONPATH="$PYTHONPATH:/home/timlangeman/webapps/neotext/neotext"
    [view python path](http://stackoverflow.com/questions/1489599/how-do-i-find-out-my-python-path-using-python)
  * > python manage.py syncdb


## Dependencies ##
  * Python 3.4, django 1.8, postgres
  * [django-cors-headers](https://github.com/ottoyiu/django-cors-headers/) (included)

## Changelog ##

v0.01 - initial release (not yet)

## Credits ##

A shoutout to everyone who has contributed:

