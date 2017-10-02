# LX WordNet Browser

## a web based browser for any individual wordnet
## and for a Pluricentric Global Wordnet


## Introduction

LX WordNet Browser is a wordnet web browser, permitting the consultation of the contents of any wordnet that follows the Princeton wordnet format. 
The browser was designed with the functionalities and interactions necessary for a new notion of pluricentric global wordnet. 

Two versions are distributed that aim to achieve different tasks. One makes it possible to consult wordnet contents of a wordnet of choice, as long as it follows the Princeton wordnet format. At any point of the search, the concepts that the user finds can be directly translated into other languages, if such concept is available. The minimalist user interface can be rendered in multiple languages. At this moment, there are two languages supported: Portuguese and English. With the efforts of the community, we wish to expand this offer to many more languages, if you are interested in helping translate the interface, read more about it [here](https://github.com/nlx-group/LX-WordNetBrowser/wiki/Translations,-a-community-helping-hand).

The other version of distribution was developed under the pluricentric global wordnet concept. It features all of the functionalities described above with a search function that is refined for multi-wordnet search. Instead of the search scope being limited to a single wordnet, the user can search for the concept in any language and have it being displayed. The browser will identify which language - wordnet the word belongs to, solving conflicts if necessary, and display the results. 

### Feature Recap

+ Single and Multi-Wordnet simultaneous search
+ Lemma relations can be selected and explored.
+ Multilingual user interface
+ Translations into selected languages
+ Web-based platform independent


## Installation

The first step is to download the .zip file of the LX-WordNetBrowser and unpack it at your desired location. 

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

In langdata/main you should be putting your wordnet files in, along with the respective bridge between the pivot language.

More configuration coming soon, for the mean time this is strictly a development configuration.
## Run

To run the server, make sure to have your working directory inside your project folder. To start the server, run the following command ```python manage.py runserver IP:PORT```.

Forthcoming: Integration with Apache web server for a production grade configuration.

