Installation
============

The first step is to download the .zip file of the LX-WordNetBrowser and unpack it at your desired location.

Requirements
------------

To install and run this browser you need to have `Python <https://www.python.org/downloads//>`_ 3.6.3 installed (or the most recently available).

To install the required dependencies cd to the folder extracted from the .zip file you downloaded and run the following command: ``pip3 install -r requirements.txt.``

With all the dependencies installed, you can start to configure the wordnet browser.

CD to the folder where your project is, and execute the command ``django-admin.py startproject webapp``.

Copy the folders on the downloaded code (not requirements.txt) into the folder your project is on.

Configuration
-------------

General File Config
^^^^^^^^^^^^^^^^^^^

On settings.py under the webapp folder, insert the following:

- In INSTALLED_APPS list, add 'search' to the list
- At the end, paste the following code:

.. code-block:: python

	STATICFILES_DIRS = [
    	os.path.join(BASE_DIR, "static"),
	]

	STATIC_URL = '/static/'


substitute STATICFILES_DIRS if it's there already.

- In TEMPLATES, you will find 'DIRS' likely empty, substitute it with the following:
	[os.path.join(BASE_DIR, 'templates')]
- In ALLOWED_HOSTS, insert the IP you're going to use for your website.

- In webapp/urls.py, paste the following code:

.. code-block:: python

	from django.conf.urls import include, url
	from django.contrib import admin
	from search import urls

	urlpatterns = [
	    url(r'^admin/', admin.site.urls),
	    url(r'^', include(urls)),
	    
	]

In /static/index.js search for "location.port", if you are using a domain you will likely not need the port so delete the ':' + location.port occurances and leave just the location.hostname. Still in index.js, for the pluricentric installation, you will want to edit the const "nodeText" to fit your institution name.

In langdata/main you should be putting your wordnet files in, along with the respective bridge between the pivot language.

Back to /static/views.py, search for 'display limit', which will be a comment section. There you will need to decide whether you will limit the results to be shown and the number of depth you will limit it by. If not, then you will set depth to None.

WordNet Content Delivery Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To avoid opening and reading wordnet files everytime there's a request, we'll setup a WordNet content delivery server. The code for this server is contained in 'wordnet_server.py'.

Give run permissions to wordnet_server.py if on a unix system using ``chmod u+x wordnet_server.py``. Here's the command line syntax: ``wordnet_server.py [PORT] [BROWSER_PATH] [BROWSER_TYPE]``.

PORT is the port you'll be using for **Wordnet CDN Server, do not use the port you're using for the wordnet browser**. 

BROWSER_PATH is the path to the project folder where you have your browser. If you have the wordnet_server.py file in it you can just use '.'. 

BROWSER_TYPE has two options: pluricentric or basic. These referring to the two types of installations supplied. If you want to use this server to serve a pluricentric web browser, use pluricentric. If it's supplying a 'my_wordnet' type of installation, use basic.

Once you have configured your server, make sure to edit the file ``/search/views.py`` corresponding to your project to be able to access the right port. By searching 'wordnet_server', you will find the inicialization of the server. The port side of URL is empty so you can edit and put in the port you have chosen.

The configuration currently uses localhost as the IP of the CDN server. If you wish to have an external server as a host, you will have to edit the code in order to use the right IP and port.

If you have the two installations running you will have to have seperate CDN servers for each installation by using different ports and editing the views.py code to match them.

Apache Configuration
--------------------

Forthcoming.

Run
^^^

To run on a development environment, cd int the project directory and run the following command ``python manage.py runserver IP:PORT``.	

