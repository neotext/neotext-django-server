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

## Setup/Installation Instructions: ##
  * Python 3.4 or higher is required

### Windows Installation ###
  * Clone the Git Repository (with GitHub Desktop Client):
    - Download the [GitHub Desktop Client](https://desktop.github.com/) if you don't have it already.
    - Make sure you're logged in when using the client
    - Click the Green "Open in Desktop" link
    - Click "Clone in Desktop"
  * Setup Virtual Environment:
      1. Open a Command Prompt in the Directory where you Cloned the Project
      pip install virtualenv
        - If you get a Permission Denied Error when installing Virtual Environment
          PermissionError: [Errno 13] Permission denied: 'c:\\program files\\python36\\Lib\\site-packages\\virtualenv.py'

        - You have to be able to write to the folder that you're installing it to
            http://stackoverflow.com/questions/31172719/pip-install-access-denied-on-windows

      2. Create a New Virtual Environment
        virtualenv neotextEnv  (where neotextEnv is the name of the environment)
      3. [Activate the Virtual Environment](http://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate
) on Windows:
        - neotextEnv\Scripts\activate.bat

        - You should see your command prompt say:
          * (neotextEnv) C:\Path\To\Repositories

  * Go to the main folder containing requirements.txt:
      - pip install -r requirements.txt
  * [Add your own neotext folder to the python path](http://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7)
	 - create a Python Path variable if you don't have one already
   - [view python path](http://stackoverflow.com/questions/1489599/how-do-i-find-out-my-python-path-using-python)
   * Setup your own Database & AWS Credentials in settings.py
      - copy settings.default.py to settings.py
   * Create Postgres Database (optional: it will use SQLlite otherwise):
     - if using SQLlite, there is no need to edit the settings file
     - if using Postgres, [Download Postgres](https://www.postgresql.org/download/windows/) if you don't have it
      * run the Postgres installer
      * create new database and user,
      * note the Postgres database name and password
     - edit the Postgres database password in settings.py

   * Create the Database Tables (all database types)
     - python manage.py syncdb


### Mac/Linux Installation ###
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
   - copy settings.default.py to settings.py
* Create Postgres Database (optional: it will use SQLlite otherwise):
  - if using SQLlite, there is no need to edit the settings file
  - if using Postgres, create new database and user,
  - note the Postgres database name and password
  - edit the Postgres database password in settings.py

* Create the Database Tables (all database types)
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
