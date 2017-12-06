Developer Documentation - Pluricentric WordNet
==============================================

Back end
---------

Views.py
^^^^^^^^
The main different between pluricentric and my wordnet type of installations is the fact that you can search in *any of the implemented languages* and it will display results if such are found. It will identify the language and then display the results.

Language identifying is done with **language_identifier**, being as simple as going through index files and seeing if the word shows up on them. Due to being a single word search, other sofisticated techniques of language identification don't work as well.
If there's a collision, as in more than one languages are detected, then a message will be sent to the client for him/her to decide the language he/she wants to explore.

The advanced search for a translation can be done either through a pair file if there's one present, where the translation is then between synsets. If one isn't present, a search will be done through tab files. If there's more than one sense detected, a pairing mismatch error will happen as it is uncertain which sense of the lemma the source language synset is in the target language.

Front End
---------

language.js
^^^^^^^^^^^
There's additions to language.js as more menus come up, such as the language collision pop-up.

index.js
^^^^^^^^
Similar to the views.py, the only addition done is the collision treatment. If javascript receives a collision message, it will render a pop-up for the user to decide which language he/she wants to explore, that gets sent back to the server. Now that the server knows the language, the processes are the same as a my wordnet type installation.
