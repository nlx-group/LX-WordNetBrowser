[![Documentation Status](https://readthedocs.org/projects/lx-wordnetbrowser/badge/?version=latest)](http://lx-wordnetbrowser.readthedocs.io/en/latest/?badge=latest)
# LX WordNet Browser

## a web based browser for any individual wordnet
## and for a Pluricentric Global Wordnet


## Introduction

LX WordNet Browser is a wordnet web browser, permitting the consultation of the contents of any wordnet that follows the Princeton wordnet format. 
The browser was designed with the functionalities and interactions necessary for a new notion of pluricentric global wordnet. 

Two versions are distributed that aim to achieve different tasks. One makes it possible to consult wordnet contents of a wordnet of choice, as long as it follows the Princeton wordnet format. At any point of the search, the concepts that the user finds can be directly translated into other languages, if such concept is available. The minimalist user interface can be rendered in multiple languages. At this moment, there are two languages supported: Portuguese and English. With the efforts of the community, we wish to expand this offer to many more languages, if you are interested in helping translate the interface, read more about it [here](http://lx-wordnetbrowser.readthedocs.io/en/latest/translations.html).

The other version of distribution was developed under the pluricentric global wordnet concept. It features all of the functionalities described above with a search function that is refined for multi-wordnet search. Instead of the search scope being limited to a single wordnet, the user can search for the concept in any language and have it being displayed. The browser will identify which language - wordnet the word belongs to, solving conflicts if necessary, and display the results. 

### Feature Recap

+ Single and Multi-Wordnet simultaneous search
+ Lemma relations can be selected and explored.
+ Multilingual user interface
+ Translations into selected languages
+ Web-based platform independent

## Support Documentation

All of the support documentation for this interface is found at https://lx-wordnetbrowser.readthedocs.io. It features installation steps, user and development documentation. It is highly advised you read them if you want to set up your own node.

## Installation

The first step is to download the .zip file of the LX-WordNetBrowser and unpack it at your desired location. Ignore the folder docs, you won't need it and can delete it.

### Requirements

To install and run this browser you need to have [Python](https://www.python.org/downloads/) 3.6.3 installed (or the most recently available). 

<!--
It is recommended that you install the required dependencies in a virtual environment. To do so, first install virtualenv by running the following command: ```pip3 install virtualenv```.

To create a virtual environment, run the following command: ```virtualenv [browser folder path]```, or cd to the browser folder path and run ```virtualenv . ```.

To activate the virtualenv, cd into the browser folder and run ```source bin/activate``` and ```deactivate```to exit the virtualenv on UNIX systems. For windows, to activate ```Scripts/activate``` and ```deactivate``` to exit.

Once inside your virtual environment (or not if chose not to do it), 
-->

To install the required dependencies cd to the folder extracted from the .zip file you downloaded and run the following command: ```pip3 install -r requirements.txt```.

<!--
You will need to have the virtual environment activated while the web server is online.
-->

With all the dependencies installed, you can start to configure the wordnet browser.

CD to the folder where your project is, and execute the command ```django-adming.py startproject webapp```.

Copy the folders on the downloaded code (not requirements.txt) into the folder your project is on. 

### Configuration

On settings.py under the webapp folder, insert the following:

+ In INSTALLED_APPS list, add 'search' to the list
+ At the end, paste the following code:
```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'
```
substitute STATICFILES_DIRS if it's there already.
+ In TEMPLATES, you will find 'DIRS' likely empty, substitute it with the following:
```python
[os.path.join(BASE_DIR, 'templates')]
```
+ In ALLOWED_HOSTS, insert the IP you're going to use for your website.

+ In webapp/urls.py, paste the following code:
```python
from django.conf.urls import include, url
from django.contrib import admin
from search import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(urls)),
    
]
```

In /static/index.js search for “location.port”, if you are using a domain you will likely not need the port so delete the ‘:’ + location.port occurances and leave just the location.hostname. Still in index.js, for the pluricentric installation, you will want to edit the const “nodeText” to fit your institution name.

In langdata/main you should be putting your wordnet files in, along with the respective bridge between the pivot language.

**IMPORTANT** Read the following section in this document(http://lx-wordnetbrowser.readthedocs.io/en/latest/developer-documentation-general.html#files) of developer documentation to understand how the file locations and format works.


### WordNet Content Delivery Server

To avoid opening and reading wordnet files everytime there’s a request, we’ll setup a WordNet content delivery server. The code for this server is contained in ‘wordnet_server.py’.

Give run permissions to wordnet_server.py if on a unix system using ```chmod u+x wordnet_server.py```. Here’s the command line syntax: ```wordnet_server.py [PORT] [BROWSER_PATH] [BROWSER_TYPE]```.

PORT is the port you’ll be using for Wordnet CDN Server, do not use the port you’re using for the wordnet browser.

BROWSER_PATH is the path to the project folder where you have your browser. If you have the wordnet_server.py file in it you can just use ‘.’.

BROWSER_TYPE has two options: pluricentric or basic. These referring to the two types of installations supplied. If you want to use this server to serve a pluricentric web browser, use pluricentric. If it’s supplying a ‘my_wordnet’ type of installation, use basic.

Once you have configured your server, make sure to edit the file ```/search/views.py``` corresponding to your project to be able to access the right port. By searching ‘wordnet_server’, you will find the inicialization of the server. The port side of URL is empty so you can edit and put in the port you have chosen.

The configuration currently uses localhost as the IP of the CDN server. If you wish to have an external server as a host, you will have to edit the code in order to use the right IP and port.

If you have the two installations running you will have to have seperate CDN servers for each installation by using different ports and editing the views.py code to match them.
## Run

To run the server, make sure to have your working directory inside your project folder. To start the server, run the following command ```python manage.py runserver IP:PORT```.

To run on a production environment, refer to the explanation below. The website will be reachable on your IP port 80.

## Apache Configuration

We are going to use Apache on the front end of the server that is going to act as a reverse proxy to a WSGI server running on gUnicorn.

## gUnicorn Installation and Setup

To install gUnicorn simply run the command ``pip3 install gunicorn``.

Setup/run is extremely easy, just run the command ``gunicorn projectname.wsgi`` in your project folder and it will start up the server. The server is started on 127.0.0.1:8000.

More info here: https://docs.djangoproject.com/ko/1.11/howto/deployment/wsgi/gunicorn/

## Apache Reverse Proxy

If you don't have apache2 on your machine, you can either scour through the web for the installer if you're on a Windows machine or if you're on ubuntu you can most likely install it through ``apt-get install apache2``.

Create a configuration file on sites-available, on ubuntu it's on ``/etc/apache2/sites-available``, the content should be the following:

```apacheconf
<VirtualHost *:80>

		ServerAdmin email

		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined

		ProxyPass /static/ !
		ProxyPass / http://localhost:8000/

		Alias /static/ COMPLETE_PATH_TO_YOUR_PROJECT_STATIC_FOLDER

		<Directory COMPLETE_PATH_TO_YOUR_PROJECT_STATIC_FOLDER>
			Options Indexes FollowSymLinks
			AllowOverride None
			Require all granted
		</Directory>
	</VirtualHost>
```
After creating your config file run the following commands:

``sudo a2dissite 000-default`` and ``sudo a2ensite [config_file_name]`` name without extension. Then to restart apache2 run ``sudo apache2ctl restart``.

And it should be serving everything correctly.
