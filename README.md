# LX-WordNetBrowser

## a web based browser for any individual wordnet
## and for a Pluricentric Global Wordnet


## Introduction

page under construction


## Installation

The first step is to download the .zip file of the LX-WordNetBrowser and unpack it at your desired location. 

### Requirements

To install and run this browser you need to have the [Python](https://www.python.org/downloads/) 3.6.3 installed. 

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

+ In INSTALLED_APPS list, add 'search'
+ At the end, paste the following code:
```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'
```
substitute STATICFILES_DIRS if it's there already.


## Run

to complete

