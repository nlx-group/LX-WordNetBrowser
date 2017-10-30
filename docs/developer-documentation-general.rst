Developer Documentation - General
====================================

Back end
---------

WordNet Content Delivery Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The WordNet content delivery server is implemented using XMLRPC protocol, which despite worries about its unsafety, is a good candidate due to its simplicity of implementation and usability. It being hosted on localhost mitigates the safety worries.

As specified in the installation chapter, there's two modes to this server. It can either load and supply a pluricentric or a my wordnet type of installation. Upon launch of the server, it will call 2 loaders of its own, that load tab files and wordnet files. The difference between the modes are on the amount of wordnets it has to load and their locations, which are different from the pluricentric and my wordnet type of installations.

The structure in which the wordnet is stored is a dictionary with the following structure.

language > pos > data & index > offset > whole line.

language on the my wordnet installation is main for the main language and pivot for the pivot language.

This implementation could be improved by instead of storing a whole line, storing a dictionary for each offset with the relations present and with what offsets, names, and other info that is further used in searches.

For vrb files, the structure is the following:

language > vrb > verb OR number of sent/frame > line.

For the tab files, it follows the following structure:

language code > pivot language offset > line.

Other methods, such as get_index and get_data are implemented for the main script /search/views.py fetch information needed relevant to the users search.

Apache
^^^^^^
Forthcoming

Django
^^^^^^
Django is the framework chosen to power the interface. Since there's a server to deliver wordnet content, any functionalities related to databases aren't touched. There's little need for an admin portal as well, so it's up to other developers to implement one if there's any need for them.

Views.py
^^^^^^^^
Classes
#######

Parser
######
Defines a class for parsers of lines. This is where the wordnet lines get converted to HTML formatted lines with all the relevant information such as names and glosses. All search functions other than translations will eventually call this class to format their lines or obtain information

Search Routines
###############
This class holds all the search routines that are needed for the browser to work. 

Single search is used only in one special case, which is when you explore derivationally related forms and you wish to see, for a given result, what its synset looks like. In that case, **single_search** will be called to deliver just the one synset its looking for, not a lemma driven search.

**full_search** is the most commonly used method for post initial lemma driven searches. After the user searches for a lemma and its results appear on the screen, they may expand the relations menu, as explained in :doc:`user-documentation`, and through that navigate the various relations that the synset may have with others. That relation targeting is handled by full_search alone.
It will take the synset and search, recursively, through the synsets that hold the type of relation targeted in the search. It is essentially going through the graph all the way to the bottom of each branch. In the end, an HTML list is built by constantly concatenating the information of each synset.
There's the notion of max_length and max_depth. Max_length is the maximum of local(synset) relations that can be displayed, and max_depth is the depth of the graph that you can get to. These can be equal to None if you don't want to maximize the display of results, this is just a "safety" feature to avoid scraping of wordnets that may be unwanted by the holders.
Throughout the search, information on what relations are present in each synset will be stored and sent over. This information will be stored in the javascript process to be faster in understanding what relations are present in each synset upon a relations menu expansion.

**expand_search** is just a work delegator, it identifies what the request wants and distributes it to the functions inside the search routines appropriate to the request.

**sentence_frame_search** searches for a certain verbs sentence frames. They may be specific or general frames.

**normal_search** follows a similar strategy to **full_search**, albeit being a iterative, 0 depth search. It will search for the lemma being searched for in the index file and then with the offsets now in hand, the data info will be retrieved and parsed to an html line to be delivered. The information regarding present relations are also sent over.

Renders
#######

The class renders has the methods that render the webpage to the user, upon a visit.

Front End
---------

language.js
^^^^^^^^^^^
Due to how little text menu oriented the interface is, instead of having dozens of repeated files, one for each language that the interface offers, we decided to use a javascript object structured file with all the text. This can be done differently by other developers who may take on this interface by having actual URLs that direct to different configurations.

The text is then loaded by language and by context. It can be a part of speech translation, or a part of the menu relating to semantic relations, etc.

index.js
^^^^^^^^
The **main** as one would expect loads all the dependencies, event listeners of all sorts that are needed for the UI to work. If the user searches for a lemma, **search** is called which appends a box for the results to be displayed and issues a GET request, whose response is treated in **formattedResults**.

If the user wants to expand the related concepts menu, **expand** is called which will check what relations are present in that offset and display the possible searches. If the user then selects one of those relations, **expandedSearch** is called. This function checks if the search was already done in the past, which if that's the case, it will hide the results (the user may not be interested in that result anymore and wants to keep his window clean of it), otherwise it will issue a GET request for the search. The result from that GET request then get treated by **expandedSearchFormatter** unless its a sentence frame, whose function **sentenceFrameFormatter** does the work for.