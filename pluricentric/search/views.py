from django.http import JsonResponse
from django.shortcuts import render
import json
import logging
import xmlrpc.client


pointer_map = {'Hypernym': '@', 'Hyponym': '~', 'Member_Holonym': '#m', 'Substance_Holonym': '#s', 'Part_Holonym': '#p',
               'Member_Meronym': r'%m', 'Substance_Meronym': r'%s', 'Part_Meronym': r'%p', 'Antonym': '!',
               'Instance_Hypernym': '@i', 'Instance_Hyponym': '~i', 'Attribute': '=',
               'Derivationally_related_form': '+',
               'Entailment': '*', 'Cause': '>', 'Also_see': '^', 'Verb_Group': '$', 'Similar_to': '&',
               'Participle_of_verb': '<', 'Pertainym': '\\', 'Domain_Category': ';c', 'Domain_Term_Category': '-c',
               'Domain_Region': ';r', 'Domain_Term_Region': '-r', 'Domain_Usage': ';u', 'Domain_Term_Usage': '-u'}

pointer_name_map = {'ihype': 'Hypernym', 'dhype': 'Hypernym', 'fhypo': 'Hyponym', 'dhypo': 'Hyponym',
                    'mh': 'Member_Holonym',
                    'sh': 'Substance_Holonym', 'ph': 'Part_Holonym', 'mm': 'Member_Meronym', 'sm': 'Substance_Meronym',
                    'pm': 'Part_Meronym', 'ant': 'Antonym', 'inhype': 'Instance_Hypernym', 'inhypo': 'Instance_Hyponym',
                    'attr': 'Attribute', 'derform': 'Derivationally_related_form', 'ent': 'Entailment', 'ca': 'Cause',
                    'asee': 'Also_see', 'vgr': 'Verb_Group', 'sto': 'Similar_to', 'pverb': 'Participle_of_verb',
                    'per': 'Pertainym', 'domcat': 'Domain_Category', 'domtermcat': 'Domain_Term_Category', 'domreg':
                        'Domain_Region', 'domtermreg': 'Domain_Term_Region', 'domusage': 'Domain_Usage', 'domtermusage':
                        'Domain_Term_Usage'}

part_of_speech = {'n': 'noun', 'v': 'verb', 'a': 'adj', 's': 'adj', 'r': 'adv'}

language_codes = {'English': 'en', 'Finnish': 'fin', 'Afrikaans': 'afr', 'Arabic': 'arb', 'Asturian': 'ast',
                  'Azerbaijani': 'aze', 'Belarusian': 'bel', 'Bengali': 'ben', 'Breton': 'bre', 'Bulgarian': 'bul',
                  'Catalan': 'cat', 'Czech': 'ces', 'Chinese': 'cmn', 'Welsh': 'cym', 'Danish': 'dan', 'German': 'deu',
                  'Greek': 'ell', 'Esperanto': 'epo', 'Estonian': 'est', 'Basque': 'eus', 'Faroese': 'fao',
                  'Farsi': 'fas', 'French': 'fra', 'Scottish Gaelic': 'gla', 'Irish': 'gle', 'Galician': 'glg',
                  'Serbo-Croatian': 'hbs', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Indonesian': 'ind',
                  'Icelandic': 'isl', 'Italian': 'ita', 'Japanese': 'jpn', 'Georgian': 'kat', 'Korean': 'kor',
                  'Latin': 'lat', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Macedonian': 'mkd', 'Dutch': 'nld',
                  'Nynorsk': 'nno', 'Bokmål': 'nob', 'Polish': 'pol', 'Romanian': 'ron', 'Russian': 'rus',
                  'Slovak': 'slk', 'Slovene': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe',
                  'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd',
                  'Vietnamese': 'vie', 'Volapük': 'vol', 'Malaysian': 'zsm', 'Taiwan Chinese': 'qcn',
                  'Português': 'por'}

code_to_language = {
    'en': 'English', 'fin': 'Finnish', 'afr': 'Afrikaans', 'arb': 'Arabic', 'ast': 'Asturian', 'aze': 'Azerbaijani',
    'bel': 'Belarusian', 'ben': 'Bengali', 'bre': 'Breton', 'bul': 'Bulgarian', 'cat': 'Catalan', 'ces': 'Czech',
    'cmn': 'Chinese', 'cym': 'Welsh', 'dan': 'Danish', 'deu': 'German', 'ell': 'Greek', 'epo': 'Esperanto',
    'est': 'Estonian', 'eus': 'Basque', 'fao': 'Faroese', 'fas': 'Farsi', 'fra': 'French', 'gla': 'Scottish Gaelic',
    'gle': 'Irish', 'glg': 'Galician', 'hbs': 'Serbo-Croatian', 'heb': 'Hebrew', 'hin': 'Hindi', 'hun': 'Hungarian',
    'ind': 'Indonesian', 'isl': 'Icelandic', 'ita': 'Italian', 'jpn': 'Japanese', 'kat': 'Georgian', 'kor': 'Korean',
    'lat': 'Latin', 'lav': 'Latvian', 'lit': 'Lithuanian', 'mkd': 'Macedonian', 'nld': 'Dutch', 'nno': 'Nynorsk',
    'nob': 'Bokmål', 'pol': 'Polish', 'ron': 'Romanian', 'rus': 'Russian', 'slk': 'Slovak', 'slv': 'Slovene',
    'spa': 'Spanish', 'swa': 'Swahili', 'swe': 'Swedish', 'tel': 'Telugu', 'tha': 'Thai', 'tur': 'Turkish',
    'ukr': 'Ukrainian', 'urd': 'Urdu', 'vie': 'Vietnamese', 'vol': 'Volapük', 'zsm': 'Malaysian',
    'qcn': 'Taiwan Chinese',
    'por': 'Português'
}

pivot_language = 'English'  # Pivot language
wordnet_server = xmlrpc.client.ServerProxy('http://127.0.0.1:9004')  # Change port to the one you're using


class Parsers:
    def __init__(self, line=None):
        self.line = line
        self.split_line = (line.split() if line is not None else None)

    @staticmethod
    def line_parser(split_line, line, offset, search_type, history):
        """
        Creates an HTML line for the synset display.

        Requires: line is a string, offset is a string, split_line is a list of strings, search_type is a string
        history is a a list of strings.
        Ensures: A string that is in HTML form, ready to be displayed.
        """
        if search_type != 'derform':  # Check if the search type(relation) is derivationally related form
            # html_line creates a string in html format with the names separated by a comma
            # split_line[4:4 + int(split_line[3], 16) * 2:2] gets all the names
            html_line = '<li class="' + offset + '-' + split_line[
                2] + '"><a class="concept" data-tool-tip="tooltip" style="cursor:pointer">rels </a> <span style="color:red">(' + \
                        split_line[2] + ')</span>' + ''.join(
                [' ' + '<span class="mark">' + name.replace('_', ' ') + '</span>' + ',' for name in
                 split_line[4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + split_line[
                            4 + int(split_line[3], 16) * 2 - 2].replace('_', ' ') + '</span>'
            gloss_split = line.split('|')[1].split(';')  # Get the gloss by splitting the line by '|'
            # Descriptions concatenated with examples gives you the whole formatted gloss
            descriptions = list(
                map(lambda x: x[(1 if x[0] == ' ' else 0):], list(filter(lambda x: '"' not in x, gloss_split))))
            examples = list(filter(lambda x: '"' in x, gloss_split))
            html_line += ' (' + ';'.join(descriptions).rstrip() + ') ' + ';'.join(
                list(map(lambda x: '<span style="font-style:italic">' + x + '</span>', examples)))
            return html_line
        else:
            html_line = '<li class="' + offset + '-' + split_line[
                2] + '"><a class="concept" data-tool-tip="tooltip" style="cursor:pointer">rels </a> <span style="color:red">(' + \
                        split_line[2] + ')</span>'
            # Derivationaly related forms have source lemma and target lemma, that have to be identified
            source_word, target_word = ('', '')
            for i in range(5 + int(history[3], 16) * 2,
                           5 + int(history[3], 16) * 2 + int(history[4 + int(history[3], 16) * 2]) * 4, 4):
                if history[i + 1] == offset:
                    # Search for the relation that targets synset and choose the target word
                    source_word, target_word = (int(history[i + 3][0:2]), int(history[i + 3][2:]))
                    break
            if target_word == 0:
                # If target word is 00 then it means its targeting all lemmas
                html_line += ''.join([' ' + '<span class="mark">' + name.replace('_', ' ') + '</span>' + ',' for name in
                                      split_line[
                                      4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + \
                             split_line[4 + int(split_line[3], 16) * 2 - 2].replace('_', ' ') + '</span>'
            else:
                # Else target word indice
                html_line += '<span class="mark"> ' + split_line[4:4 + int(split_line[3], 16) * 2:2][
                    target_word - 1].replace(
                    '_', ' ') + '</span>'
            if source_word == 0:
                # If source word is 00 then its targeting all lemmas
                html_line += ' [<span class="derformMark"></span>' + ''.join([' ' + '<span class="mark">' +
                                                                              name.replace('_', ' ') + '</span>' + ','
                                                                              for name in history[4:4 + int(history[3],
                                                                                                            16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + \
                             history[4 + int(history[3], 16) * 2 - 2].replace('_', ' ') + '</span>]'
            else:
                # Else target word indice
                html_line += ' [<span class="derformMark"></span> ' + '<span class="mark">' + \
                             history[4:4 + int(history[3], 16) * 2:2][
                                 source_word - 1].replace('_', ' ') + '</span>]'
            # Gloss routine like above
            gloss_split = line.split('|')[1].split(';')
            descriptions = list(
                map(lambda x: x[(1 if x[0] == ' ' else 0):], list(filter(lambda x: '"' not in x, gloss_split))))
            examples = list(filter(lambda x: '"' in x, gloss_split))
            html_line += ' (' + ';'.join(descriptions).rstrip() + ') ' + ';'.join(
                list(map(lambda x: '<span style="font-style:italic">' + x + '</span>', examples)))
            return html_line

    def pointers(self):
        """
        Returns a list whose indices are the indices of the positions of pointers in a data line.
        """
        return range(5 + int(self.split_line[3], 16) * 2,
                     5 + int(self.split_line[3], 16) * 2 + int(
                         self.split_line[4 + int(self.split_line[3], 16) * 2]) * 4, 4)

    def names(self):
        """
        Returns a list of names in the data line.
        """
        return self.split_line[4:4 + int(self.split_line[3], 16) * 2:2]

    def frames(self):
        """
        Returns a list of the frames for a given verb data line.
        """
        word_count = int(self.split_line[3], 16)
        pointer_count = int(self.split_line[3 + word_count * 2 + 1])
        frames_count = int(self.split_line[word_count * 2 + pointer_count * 4 + 5])
        return list(map(lambda x: str(int(x)), self.split_line[
                                               7 + word_count * 2 + pointer_count * 4: 7 + word_count * 2 + pointer_count * 4 + 3 * frames_count: 3]))

    def offsets(self):
        """
        Returns a list of offsets.
        """
        return self.split_line[3 + int(self.split_line[3]) + 3:]

    def relations(self):
        """
        Returns a list of relation pointers.
        """
        return self.split_line[5 + int(self.split_line[3], 16) * 2:5 + int(self.split_line[3], 16) * 2 + int(
            self.split_line[4 + int(self.split_line[3], 16) * 2]) * 4:4]


class SearchRoutines:
    def __init__(self, offset=None):
        self.offset_holder = offset

    @staticmethod
    def single_search(language, offset, pos, search_type):
        """
        Performs a search for an offset in a language.

        Requires: Language is a string, offset is a string, pos is a string, search_type is a string.
        Ensures: A dictionary with an HTML formatted line, having line as its key and a dictionary with
        the relations present in that offset with relations as its key.
        """
        relations = {part_of_speech[pos]: {offset: []}}  # Relations dictionary organised by POS
        line = ''  # HTML Line
        synset_line = Parsers(wordnet_server.get_data(language, part_of_speech[pos], offset))  # Instanciate the parser
        split_line = synset_line.split_line  # Get the list of the line split
        for i in synset_line.pointers():
            if split_line[i] not in relations[part_of_speech[pos]][offset]:
                # If the relation isn't recorded yet in the POS:Offset, add it in
                relations[part_of_speech[pos]][offset].append(split_line[i])
        line += '<ul>' + Parsers.line_parser(split_line, synset_line.line, offset, search_type, '') + '</ul>'
        return {'line': line, 'relations': relations}

    def full_search(self, language, pos, offset, search_type, depth, history, max_depth=None, max_length=None):
        """
        Performs a full search of the tree, starting from an initial offset and either going up or down the tree,
        passing by each branch till the end if max_depth is none otherwise it will restrict the search to a certain
        depth.

        Requires: Language, pos, offset, search_type, depth are strings. max_depth and max_lenght are ints.
        History is a string at first, being initialized as an empty string but will after the first run be a list
        of strings instead.
        Ensures: A dictionary containing 2 pairs of key, values. One key containing a dictionary which contains an HTML
        formatted line of the search and the other key containing another dictionary which serves as referral
        dictionaries, having each offset map and the relations it has.
        """
        pointer = pointer_map[pointer_name_map[search_type]]  # Get the pointer symbol
        relations = {}  # relations for POS:SYNSET
        line = ''  # HTML Line
        first = True
        idnum2 = 0  # Just a counter for indices
        synset_line = Parsers(wordnet_server.get_data(language, part_of_speech[pos], offset))  # Instanciate the parser
        split_line = synset_line.split_line  # Get the split line
        relations_offset = []
        for i in synset_line.pointers():
            if part_of_speech[pos] not in relations:
                # If the POS isn't in relations yet, let's add it in
                relations[part_of_speech[pos]] = {}
            if split_line[i] == pointer:
                # If the pointer targeted is the same pointer for the relation search, add the synset offset to the list
                # relations_offset to display results and go further down the graph
                relations_offset.append(split_line[i + 1] + '-' + split_line[i + 2])
            if split_line[0] not in relations[part_of_speech[pos]]:
                # If the current synset(split_line[0]) isn't in the relations dictionary, it gets added
                relations[part_of_speech[pos]][split_line[0]] = [split_line[i]]
            else:
                if split_line[i] not in relations[part_of_speech[pos]][split_line[0]]:
                    # Else if the relation pointer isn't in the relations table, it gets added to POS:Synset
                    relations[part_of_speech[pos]][split_line[0]].append(split_line[i])
        max_local_length = 0
        if max_length is not None:
            # This is one of the restrictions that you can use if you don't wish to transverse the whole graph searching
            # for relations
            max_local_length = (len(relations_offset) if max_length > len(relations_offset) else max_length)
        else:
            max_local_length = len(relations_offset)
        if max_depth == None:
            if len(relations_offset) > 0:  # If there's any synsets with the relation
                for _ in range(max_local_length):
                    if first and offset != self.offset_holder:
                        # We have to differentiate between the first of this recursion due to the <ul> tags, where the
                        # First has to open and the last has to close the <ul>. Also, the synset offset cannot be the
                        # same as offset_holder which has the value of the synset in which this search was requested
                        # which doesn't need to be displayed again
                        line += '<ul>' + Parsers.line_parser(split_line, synset_line.line, split_line[0], search_type,
                                                             history)  # Line parser returns an html line of the data
                        # line
                        first = False
                    # Recursive function, it follows down the line till the end for each node
                    result = self.full_search(language, relations_offset[idnum2].split("-")[1],
                                              relations_offset[idnum2].split("-")[0], search_type,
                                              str(int(depth) + 1),
                                              (
                                                  split_line if search_type == 'derform' and history == '' else history),
                                              max_depth,
                                              max_local_length)
                    for key in result['relations']:
                        # Just updating the relations table with new information
                        if key not in relations:
                            relations[key] = {}
                        for offset in result['relations'][key]:
                            if offset not in relations[key]:
                                relations[key][offset] = result['relations'][key][offset]
                    line += result['line'] + '</li>'  # Since the parser returns an <li> that is unclosed, we close it
                    idnum2 += 1
                return {'relations': relations, 'line': line + '</ul>'}
            else:
                # If there's no synset relations then it just returns an empty relation table and returns
                if split_line[0] not in relations[part_of_speech[pos]]:
                    relations[part_of_speech[pos]][split_line[0]] = []
                line += '<ul>' + Parsers.line_parser(split_line, synset_line.line, split_line[0], search_type, history)
                return {'line': line + '</li></ul>', 'relations': relations}
        else:
            # This follows the same thought track as the branch above but this time its restricted in depth and
            # Ends the search at max_depth
            if int(depth) < max_depth:
                if first and offset != self.offset_holder:
                    line += '<ul>' + Parsers.line_parser(split_line, synset_line.line, split_line[0], search_type,
                                                         history)
                    first = False
                for _ in range(max_local_length):
                    result = self.full_search(language, relations_offset[idnum2].split("-")[1],
                                              relations_offset[idnum2].split("-")[0], search_type,
                                              str(int(depth) + 1),
                                              (
                                                  split_line if search_type == 'derform' and history == '' else history),
                                              max_depth,
                                              max_local_length)
                    for key in result['relations']:
                        if key not in relations:
                            relations[key] = {}
                        for offset in result['relations'][key]:
                            if offset not in relations[key]:
                                relations[key][offset] = result['relations'][key][offset]
                    line += result['line'] + '</li>'
                    idnum2 += 1
                if split_line[0] not in relations[part_of_speech[pos]]:
                    relations[part_of_speech[pos]][split_line[0]] = []
                return {'relations': relations, 'line': line + '</ul>'}
            else:
                return {'relations': relations, 'line': line}

    def expand_search(self, language, pos, offset, search_type):
        """
        Redirects the search to their appropriate functions, depending on whether it is a direct sibling search or full
        tree search.

        Requires: language, pos, offset, search_type are strings.
        Ensures: A dictionary resulting from the called function.
        """
        self.offset_holder = offset  # Setting a holder for the offset so its avoided on the search
        if search_type == 'con':
            return self.single_search(language, offset, pos, search_type)
        else:
            if search_type != 'fhypo' and search_type != 'ihype':
                # This is where the direct searches go, as you can see there's max_depth of 2 so it only goes to the
                # next direct node
                return self.full_search(language, pos, offset, search_type, 0, '', 2)
            else:
                if search_type == 'ihype':
                    # We chose not to restrict inherited hypernym relations
                    return self.full_search(language, pos, offset, search_type, 0, '')
                else:
                    # We chose to restrict full hyponyms however. This can be normalized for the two relations types
                    return self.full_search(language, pos, offset, search_type, 0, '', 4, 10)

    @staticmethod
    def sentence_frame_search(language, offset):
        """
        Searches for a verb synset sentence frames.

        Requires: Language is a string, offset is a string.
        Ensures: A dictionary with one key:value pair, being the HTML formatted line.
        """
        synset_line = Parsers(wordnet_server.get_data(language, 'verb', offset))  # Instanciate the parser
        html_line = '<ul class="search">'  # HTML Line
        names = []
        verbs_with_examples = {}
        for name in synset_line.names():
            # Append the lemmas from the synset line
            names.append(name)
        for name in names:
            # Get sentid from each name in a language
            line = wordnet_server.get_sentidx(language, name)
            if line is not None:
                # If the concrete sentid exists
                verbs_with_examples[name] = line.split()[1]
        if verbs_with_examples:
            # If verbs with examples exists, then there's sentid
            example_sentences = {}
            for verb in verbs_with_examples:
                for num in verbs_with_examples[verb].split(','):
                    if num not in example_sentences:
                        example_sentences[num] = ''
            for num in example_sentences:
                # For each sentence number, get line and put it in the dictionary
                line = wordnet_server.get_sents(language, num)
                example_sentences[num] = line[len(line.split()[0]) + 1:]
            for verb in verbs_with_examples:
                for sentence in verbs_with_examples[verb].split(','):
                    # Format the sentence with the verb
                    html_line += '<li>' + example_sentences[sentence] % ('<span style="font-weight:bold">' +
                                                                         verb.replace('_', ' ') + '</span>') + '</li>'
        else:
            # Else general frames are used.
            for frame in synset_line.frames():
                line = wordnet_server.get_frame(language, frame)
                if line is not None:
                    html_line += '<li>' + line[len(line.split()[0]) + 1:] + '</li>'
        return {'line': html_line + '</ul>'}

    @staticmethod
    def normal_search(language, lemma, overview=False):
        """
        Searches for a word in the wordnet files.

        Requires: Language, lemma is a string. overview is a boolean.
        Ensures: A dictionary either containing a not found message or containing HTML formatted lines and a referral
        pair of part of speeches, offsets and relations.
        """
        lemma = lemma.replace(' ', '_').lower()  # Lowercase the search word
        index_line = ''
        data_lines = []
        html_line = ''
        relations = {}
        result = {'relations': {}, 'line': ''}  # Result dictionary like seen before
        file_types = wordnet_server.pos_available(language)  # Check POS available in that language
        for pos in file_types:
            if pos != 'vrb':
                # Instanciate the parser with the index line
                synset_index = Parsers(wordnet_server.get_index(language, pos, lemma))
                index_line = synset_index.line
                if index_line is not None:
                    offsets = synset_index.offsets()
                    for offset in offsets:
                        # Append to a list the data lines of each synset whose lemma is found
                        data_lines.append(wordnet_server.get_data(language, pos, offset))
                    for line in data_lines:
                        synset_line = Parsers(line)
                        split_line = synset_line.split_line
                        line_relations = []
                        # Build the relations
                        if split_line[4 + int(split_line[3], 16) * 2] != '000':
                            for relation in synset_line.relations():
                                if relation not in line_relations:
                                    line_relations.append(relation)
                        relations[split_line[0]] = line_relations
                        # <li> for each result in each pos
                        html_line += '<li class="' + split_line[
                            0] + '-' + split_line[
                                         2] + '"><a class="concept" data-tool-tip="tooltip" style="cursor:pointer">rels </a> <span style="color:red">(' + \
                                     split_line[2] + ')</span>' + ''.join(
                            [' ' + '<span class="mark">' + name.replace('_', ' ') + '</span>' + ',' for name in
                             split_line[4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + \
                                     split_line[
                                         4 + int(split_line[3], 16) * 2 - 2].replace('_', ' ') + '</span>'
                        # Build the gloss
                        gloss_split = synset_line.line.split('|')[1].split(';')
                        descriptions = list(
                            map(lambda x: x[(1 if x[0] == ' ' else 0):],
                                list(filter(lambda x: '"' not in x, gloss_split))))
                        examples = list(filter(lambda x: '"' in x, gloss_split))
                        html_line += ' (' + ';'.join(descriptions).rstrip() + ') ' + ';'.join(
                            list(map(lambda x: '<span style="font-style:italic">' + x + '</span>', examples)))
                    # After having gone through each data line, encapsulate the <li>'s in a <ul> which pertains to
                    # The pos
                    result['line'] += ('<h2 class="pos">' + pos[0].upper() + pos[
                                                                             1:] + '</h2>' if not overview else '') + html_line + '</li>'
                    result['relations'][(pos if pos != 's' else 'adj')] = relations
                    result['found'] = 1
                    index_line = ''
                    data_lines = []
                    html_line = ''
                    relations = {}
        result['line'] = ('<h1>' + language + '</h1>' if not overview else '') + result['line']
        result['language'] = language
        result['conflict'] = 0
        result['found'] = 1
        return {'line': ["<p> The search couldn't find the word you were looking for. </p>"], 'found': 0} if not result[
            'line'] else result

    @staticmethod
    def language_identifier(lemma):
        """
        Identifies which languages the supplied lemma appears in.

        Requires: Lemma is a string.
        Ensures: There's three possible return points. Either one language is found so it returns a normal_search return
        or its found in no languages in which case it returns a 'not found' line or it's found in more than 1 language
        in which case it sends a collision flag and a list containing the languages its found in for the user to
        decide.
        """
        lemma = lemma.replace(' ', '_').lower()
        languages_available = wordnet_server.languages_available()
        languages = []
        for language in languages_available:
            # Go through each language
            pos_available = wordnet_server.pos_available(language)
            i = 0
            found = False
            while not found and i < len(pos_available):
                if pos_available[i] != 'vrb':
                    line = wordnet_server.get_index(language, pos_available[i], lemma)
                    # If there's an index line for lemma, then it means it appears in that language
                    if line is not None:
                        found = True
                        languages.append(language)
                i += 1
        if len(languages) == 1:
            # If there's only 1 language, then it's fine and goes to search
            return SearchRoutines.normal_search(languages[0], lemma)
        elif len(languages) == 0:
            # If there's none then it appears in no languages
            return {'line': ["<p> The search couldn't find the word you were looking for. </p>"], 'found': 0}
        # If none of the above then it means there's a collision, the user has to decide which language he/she wants
        return {'collision': 1, 'languages': languages}

    @staticmethod
    def advanced_search(offset, langs, pos, source_language):
        """
        Searches for translations for a given synset offset.

        Requires: Offset, pos and source language are strings. Langs is a list.
        Ensures: A dictionary with one key value pair containing html lines.
        """
        languages = json.loads(langs)
        pivot_language_offset = ''
        html_lines = {}
        lemmas = []
        pair_info_status = False
        pivot_language_offsets = []
        if pivot_language != source_language:
            pair_info = wordnet_server.get_pair(source_language, offset, pos)  # Gets pair from pair file, if exists
            if pair_info is None:
                # If no pair info, then will have to obtain information from tab files
                split_line = wordnet_server.get_data(source_language, part_of_speech[pos], offset).split()
                lemmas = split_line[4:4 + int(split_line[3], 16) * 2:2]
                tab_lines = wordnet_server.get_whole_tab(language_codes[source_language])
                for elem in tab_lines:
                    lines = tab_lines[elem]
                    for line in lines:
                        line = line.split()
                        if line[0] != '#' and line[0].split('-')[1] == pos and ' '.join(line[2:]) in lemmas:
                            pivot_language_offsets.append((' '.join(line[2:]), line[0]))
                        if len(lemmas) == len(pivot_language_offsets):
                            break
                senses = {}
                lemma_in_sense = {}
                for lemma in lemmas:
                    # Check if there's several senses found for each lemma, in which case there's a mismatch
                    for tup in pivot_language_offsets:
                        if lemma == tup[0]:
                            if tup[1] not in senses:
                                senses[tup[1]] = 1
                                lemma_in_sense[tup[1]] = [lemma]
                            else:
                                senses[tup[1]] += 1
                                lemma_in_sense[tup[1]].append(lemma)
                max_sense = [k for k, v in senses.items() if v == max(senses.values())]
                if len(max_sense) == 1:
                    pivot_language_offset = max_sense[0]
                elif len(max_sense) > 1:
                    return {'result': {'mismatch': 1}}
            else:
                # Else store pair info
                pivot_language_offset = pair_info
                pair_info_status = True
        else:
            pivot_language_offset = offset + "-" + pos
        for language in languages:
            html_lines[language] = {'lemma': [], 'def': []}
            if pivot_language_offset != '':
                if pair_info_status:
                    # If there's pair info then there's also wordnet data, so you can get the information from there
                    # Directly
                    line = wordnet_server.get_data(code_to_language[language],
                                                   part_of_speech[pivot_language_offset.split("-")[1]],
                                                   pivot_language_offset.split("-")[0])
                    split_line = line.split()
                    html_lines[language]['lemma'].append(''.join([' ' + name.replace('_', ' ') + ',' for name in
                                                                  split_line[
                                                                  4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + \
                                                         split_line[4 + int(split_line[3], 16) * 2 - 2].replace('_',
                                                                                                                ' '))
                    html_lines[language]['def'].append(''.join(
                        [split_line[split_line.index('|') + 1:][0]] + [' ' + elem for elem in
                                                                       split_line[
                                                                       split_line.index(
                                                                           '|') + 2:]]))
                else:
                    # Else gets info from the tab files
                    line = wordnet_server.get_tab(language, pivot_language_offset.split("-")[0],
                                                  pivot_language_offset.split("-")[1])
                    if line is not None:
                        synline = line[0].split()
                        html_lines[language]['lemma'].append(synline[2])
        return {'result': html_lines}


class Renders:
    @staticmethod
    def index(request):
        """
        If request comes from hostname, it renders the index HTML.
        """
        return render(request, "index.html", {})

    @staticmethod
    def help_render(request):
        """
        If request comes from hostname/help, renders help page.
        """
        return render(request, "help.html", {})

    @staticmethod
    def references_render(request):
        """
        If request comes from hostname/references, renders references page.
        """
        return render(request, "references.html", {})


class Initializer:
    @staticmethod
    def init(request):
        """
        Treats the request and redirects the query to their appropriate functions.
        """
        if request.method == 'GET' and request.is_ajax():
            request_object = request.GET
            if request_object['st'] == 'norm1' and request_object['language'] != 'UNK':
                return JsonResponse(
                    SearchRoutines.normal_search(request_object['language'], request_object['s']))
            elif request_object['st'] == 'norm1':
                return JsonResponse(SearchRoutines.language_identifier(request_object['s']))
            elif request_object['st'] == 'norm2':
                return JsonResponse(
                    SearchRoutines.normal_search(request_object['language'], request_object['s'], True))
            elif request_object['st'] == 'advsearch':
                return JsonResponse(
                    SearchRoutines().advanced_search(request_object['o'], request_object['langs'],
                                                     request_object['c'], request_object['language']))
            elif request_object['st'] == 'exp':
                return JsonResponse(
                    SearchRoutines().expand_search(request_object['language'], request_object['c'],
                                                   request_object['o'],
                                                   request_object['t']))
            elif request_object['st'] == 'stframe':
                return JsonResponse(
                    SearchRoutines().sentence_frame_search(request_object['language'], request_object['o'])
                )
        else:
            return Renders.index(request)
