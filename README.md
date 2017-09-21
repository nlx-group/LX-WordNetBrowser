# Pluricentric Global Wordnet
## A multilingual wordnet browser

*Introduction*


# Installation
First step is downloading the zip of the repository and unpacking it somewhere. After that, create a folder where you will contain the browser.
## Requirements

To be able to install and run this browser you need to have the latest [Python](https://www.python.org/downloads/) installed. 

It is recommended that you install the requirements in a virtual environment. To do so, first install virtualenv by running the following command: ```pip3 install virtualenv```.

To create a virtual environment, run the following command: ```virtualenv [browser folder path]```, or cd to browser folder path and run ```virtualenv . ```.

To activate the virtualenv, cd into the browser folder and run ```source bin/activate``` and ```deactivate```to exit the virtualenv on UNIX systems. For windows, to activate ```Scripts/activate``` and ```deactivate``` to exit.

Once inside your virtual environment (or not if chose not to do it), to install the dependancies cd to the extracted folder from the zip you downloaded and run the following command: ```pip3 install -r requirements.txt```.

You will need to have the virtual environment activated while the web server is online.

With all the dependancies installed, now we can begin to configure the web browser.

While having the working directory the folder you have your project on, execute the command ```django-adming.py startproject webapp```.

Now drag the folders you have on your downloaded code from our repository (not requirements.txt) into the folder your project is on. 

### Configurations

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



