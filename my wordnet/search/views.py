from django.http import JsonResponse
from django.shortcuts import render
import json
import os
import logging
from datetime import datetime, timedelta
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

main_language = 'English'  # Set the main language here
pivot_language = 'English'
wordnet_server = xmlrpc.client.ServerProxy('http://127.0.0.1:9004')


class Parsers:
    @staticmethod
    def line_parser(split_line, line, offset, search_type, history):
        """
        Creates an HTML line for the synset display.

        Requires: line is a string, offset is a string
        Ensures: A string that is in HTML form, ready to be displayed.
        """
        if search_type != 'derform':
            html_line = '<li class="' + offset + '-' + split_line[
                2] + '"><a class="concept" data-tool-tip="tooltip" style="cursor:pointer">rels </a> <span style="color:red">(' + \
                   split_line[2] + ')</span>' + ''.join(
                [' ' + '<span class="mark">' + name.replace('_', ' ') + '</span>' + ',' for name in
                 split_line[4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + split_line[
                       4 + int(split_line[3], 16) * 2 - 2].replace('_', ' ') + '</span>'
            gloss_split = line.split('|')[1].split(';')
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
            source_word, target_word = ('', '')
            for i in range(5 + int(history[3], 16) * 2,
                           5 + int(history[3], 16) * 2 + int(history[4 + int(history[3], 16) * 2]) * 4, 4):
                if history[i + 1] == offset:
                    source_word, target_word = (int(history[i + 3][0:2]), int(history[i + 3][2:]))
                    break
            if target_word == 0:
                html_line += ''.join([' ' + '<span class="mark">' + name.replace('_', ' ') + '</span>' + ',' for name in
                                      split_line[4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + \
                             split_line[4 + int(split_line[3], 16) * 2 - 2].replace('_', ' ') + '</span>'
            else:
                html_line += '<span class="mark"> ' + split_line[4:4 + int(split_line[3], 16) * 2:2][target_word - 1].replace(
                    '_', ' ') + '</span>'
            if source_word == 0:
                html_line += ' [<span class="derformMark"></span>' + ''.join([' ' + '<span class="mark">' +
                                                                              name.replace('_', ' ') + '</span>' + ','
                                                                              for name in history[4:4 + int(history[3],
                                                                                                            16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + \
                             history[4 + int(history[3], 16) * 2 - 2].replace('_', ' ') + '</span>]'
            else:
                html_line += ' [<span class="derformMark"></span> ' + '<span class="mark">' + \
                             history[4:4 + int(history[3], 16) * 2:2][
                                 source_word - 1].replace('_', ' ') + '</span>]'
            gloss_split = line.split('|')[1].split(';')
            descriptions = list(
                map(lambda x: x[(1 if x[0] == ' ' else 0):], list(filter(lambda x: '"' not in x, gloss_split))))
            examples = list(filter(lambda x: '"' in x, gloss_split))
            html_line += ' (' + ';'.join(descriptions).rstrip() + ') ' + ';'.join(
                list(map(lambda x: '<span style="font-style:italic">' + x + '</span>', examples)))
            return html_line


class SearchRoutines:
    def __init__(self, offset=None):
        self.offset_holder = offset

    @staticmethod
    def single_search(offset, pos, search_type):
        relations = {part_of_speech[pos]: {offset: []}}
        line = ''
        offset_line = wordnet_server.get_data('main', part_of_speech[pos], offset)
        split_line = offset_line.split()
        for i in range(5 + int(split_line[3], 16) * 2,
                       5 + int(split_line[3], 16) * 2 + int(split_line[4 + int(split_line[3], 16) * 2]) * 4, 4):
            if split_line[i] not in relations[part_of_speech[pos]][offset]:
                relations[part_of_speech[pos]][offset].append(split_line[i])
        line += '<ul>' + Parsers.line_parser(split_line, offset_line, offset, search_type, '') + '</ul>'
        return {'line': line, 'relations': relations}

    def full_search(self, pos, offset, search_type, depth, history, max_depth=None, max_length=None):
        """
        Performs a full search of the tree, starting from an initial offset and either going up or down the tree,
        passing by each branch till the end if max_depth is none otherwise it will restrict the search to a certain
        depth.

        Requires: Offset is an int, search_type, depth are strings, max_depth is int.
        Ensures: A dictionary containing 2 pairs of key, values. One key containing a dictionary which contains an HTML
        formatted line of the search and the other key containing another dictionary which serves as referral
        dictionaries, having each offset map and the relations it has.
        """
        pointer = pointer_map[pointer_name_map[search_type]]
        relations = {}
        line = ''
        first = True
        idnum2 = 0
        offset_line = wordnet_server.get_data('main', part_of_speech[pos], offset)
        split_line = offset_line.split()
        relations_offset = []
        for i in range(5 + int(split_line[3], 16) * 2,
                       5 + int(split_line[3], 16) * 2 + int(split_line[4 + int(split_line[3], 16) * 2]) * 4, 4):
            if part_of_speech[pos] not in relations:
                relations[part_of_speech[pos]] = {}
            if split_line[i] == pointer:
                relations_offset.append(split_line[i + 1] + '-' + split_line[i + 2])
            if split_line[0] not in relations[part_of_speech[pos]]:
                relations[part_of_speech[pos]][split_line[0]] = [split_line[i]]
            else:
                if split_line[i] not in relations[part_of_speech[pos]][split_line[0]]:
                    relations[part_of_speech[pos]][split_line[0]].append(split_line[i])
        max_local_length = 0
        if max_length is not None:
            max_local_length = (len(relations_offset) if max_length > len(relations_offset) else max_length)
        else:
            max_local_length = len(relations_offset)
        if max_depth == None:
            if len(relations_offset) > 0:
                for _ in range(max_local_length):
                    if first and offset != self.offset_holder:
                        line += '<ul>' + Parsers.line_parser(split_line, offset_line, split_line[0], search_type,
                                                             history)
                        first = False
                    result = self.full_search(relations_offset[idnum2].split("-")[1],
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
                return {'relations': relations, 'line': line + '</ul>'}
            else:
                if split_line[0] not in relations[part_of_speech[pos]]:
                    relations[part_of_speech[pos]][split_line[0]] = []
                line += '<ul>' + Parsers.line_parser(split_line, offset_line, split_line[0], search_type, history)
                return {'line': line + '</li></ul>', 'relations': relations}
        else:
            if int(depth) < max_depth:
                if first and offset != self.offset_holder:
                    line += '<ul>' + Parsers.line_parser(split_line, offset_line, split_line[0], search_type,
                                                         history)
                    first = False
                for _ in range(max_local_length):
                    result = self.full_search(relations_offset[idnum2].split("-")[1],
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

    def expand_search(self, pos, offset, search_type):
        """
        Redirects the search to their appropriate functions, depending on whether it is a direct sibling search or full
        tree search.

        Requires: Offset is an int, search_type, idnum and depth are strings.
        Ensures: A dictionary resulting from the called function.
        """
        self.offset_holder = offset
        if search_type == 'con':
            return self.single_search(offset, pos, search_type)
        else:
            if search_type != 'fhypo' and search_type != 'ihype':
                return self.full_search(pos, offset, search_type, 0, '', 2)
            else:
                if search_type == 'ihype':
                    return self.full_search(pos, offset, search_type, 0, '')
                else:
                    return self.full_search(pos, offset, search_type, 0, '', 4, 10)

    @staticmethod
    def sentence_frame_search(offset):
        split_line = wordnet_server.get_data('main', 'verb', offset).split()
        html_line = '<ul class="search">'
        names = []
        verbs_with_examples = {}
        for name in split_line[4:4 + int(split_line[3], 16) * 2:2]:
            names.append(name)
        for name in names:
            line = wordnet_server.get_sentidx('main', name)
            if line is not None:
                verbs_with_examples[name] = line.split()[1]
        if verbs_with_examples:
            example_sentences = {}
            for verb in verbs_with_examples:
                for num in verbs_with_examples[verb].split(','):
                    if num not in example_sentences:
                        example_sentences[num] = ''
            for num in example_sentences:
                line = wordnet_server.get_sents('main', num)
                example_sentences[num] = line[len(line.split()[0]) + 1:]
            for verb in verbs_with_examples:
                for sentence in verbs_with_examples[verb].split(','):
                    html_line += '<li>' + example_sentences[sentence] % ('<span style="font-weight:bold">' +
                                                                         verb.replace('_', ' ') + '</span>') + '</li>'
        else:
            word_count = int(split_line[3], 16)
            pointer_count = int(split_line[3 + word_count * 2 + 1])
            frames_count = int(split_line[word_count * 2 + pointer_count * 4 + 5])
            frames = list(map(lambda x: str(int(x)), split_line[
                                                     7 + word_count * 2 + pointer_count * 4: 7 + word_count * 2 + pointer_count * 4 + 3 * frames_count: 3]))
            for frame in frames:
                line = wordnet_server.get_frame('main', frame)
                if line is not None:
                    html_line += '<li>' + line[len(line.split()[0]) + 1:] + '</li>'
        return {'line': html_line + '</ul>'}

    @staticmethod
    def normal_search(lemma, overview=False):
        """
        Searches for a word in the wordnet files.

        Requires: Lemma is a string.
        Ensures: A dictionary either containing a not found message or containing HTML formatted lines and a referral
        pair of offsets and relations.
        """
        lemma = lemma.replace(' ', '_').lower()
        index_line = ''
        data_lines = []
        html_line = ''
        relations = {}
        result = {'relations': {}, 'line': ''}
        pos_available = wordnet_server.pos_available('main')
        for pos in pos_available:
            if pos != 'vrb':
                index_line = wordnet_server.get_index('main', pos, lemma)
                if index_line is not None:
                    offsets = index_line.split()[3 + int(index_line.split()[3]) + 3:]
                    for offset in offsets:
                        data_lines.append(wordnet_server.get_data('main', pos, offset))
                    for line in data_lines:
                        split_line = line.split()
                        line_relations = []
                        if split_line[4 + int(split_line[3], 16) * 2] != '000':
                            for relation in split_line[5 + int(split_line[3], 16) * 2:5 + int(split_line[3], 16) * 2 + int(
                                    split_line[4 + int(split_line[3], 16) * 2]) * 4:4]:
                                if relation not in line_relations:
                                    line_relations.append(relation)
                        relations[split_line[0]] = line_relations
                        html_line += '<li class="' + split_line[
                            0] + '-' + split_line[
                                         2] + '"><a class="concept" data-tool-tip="tooltip" style="cursor:pointer">rels </a> <span style="color:red">(' + \
                                     split_line[2] + ')</span>' + ''.join(
                            [' ' + '<span class="mark">' + name.replace('_', ' ') + '</span>' + ',' for name in
                             split_line[4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + \
                                     split_line[
                                         4 + int(split_line[3], 16) * 2 - 2].replace('_', ' ') + '</span>'
                        gloss_split = line.split('|')[1].split(';')
                        descriptions = list(map(lambda x: x[(1 if x[0] == ' ' else 0):], list(filter(lambda x: '"' not in x, gloss_split))))
                        examples = list(filter(lambda x: '"' in x, gloss_split))
                        html_line += ' (' + ';'.join(descriptions).rstrip() + ') ' + ';'.join(list(map(lambda x: '<span style="font-style:italic">' + x + '</span>', examples)))


                    result['line'] += ('<h2 class="pos">' + pos[0].upper() + pos[1:] + '</h2>' if not overview else '') + html_line + '</li>'
                    result['relations'][(pos if pos != 's' else 'adj')] = relations
                    result['found'] = 1
                    index_line = ''
                    data_lines = []
                    html_line = ''
                    relations = {}
        return {'line': ["<p> The search couldn't find the word you were looking for. </p>"], 'found': 0} if not result['line'] else result

    @staticmethod
    def advanced_search(offset, langs, pos):
        languages = json.loads(langs)
        pivot_language_offset = (offset if main_language == 'English' and pivot_language == 'English' else '')
        html_lines = {}
        # Method here to obtain pivot language offset if wordnet != Portuguese
        for language in languages:
            html_lines[language] = {'lemma': '', 'def': ''}
            if language == 'en' and pivot_language == 'English':
                line = wordnet_server.get_data('pivot', part_of_speech[pos], pivot_language_offset)
                split_line = line.split()
                html_lines['en'] = {'lemma': '', 'def': ''}
                html_lines['en']['lemma'] = ''.join([' ' + name.replace('_', ' ') + ',' for name in
                                                     split_line[4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + \
                                            split_line[4 + int(split_line[3], 16) * 2 - 2].replace('_', ' ')
                html_lines['en']['def'] = ''.join(
                    [split_line[split_line.index('|') + 1:][0]] + [' ' + elem for elem in
                                                                   split_line[
                                                                   split_line.index(
                                                                       '|') + 2:]])
            else:
                line = wordnet_server.get_tab(language, pivot_language_offset, pos)
                if line is not None:
                    line = line.split()
                    if html_lines[language]['lemma'] != '':
                        html_lines[language]['lemma'] += ', ' + line[2]
                    else:
                        html_lines[language]['lemma'] += line[2]

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
            if request_object['st'] == 'norm1':
                return JsonResponse(SearchRoutines.normal_search(request_object['s']))
            elif request_object['st'] == 'norm2':
                return JsonResponse(SearchRoutines.normal_search(request_object['s'], True))
            elif request_object['st'] == 'advsearch':
                return JsonResponse(
                    SearchRoutines().advanced_search(request_object['o'], request_object['langs'],
                                                     request_object['c']))
            elif request_object['st'] == 'exp':
                return JsonResponse(
                    SearchRoutines().expand_search(request_object['c'], request_object['o'],
                                                   request_object['t']))
            elif request_object['st'] == 'stframe':
                return JsonResponse(
                    SearchRoutines().sentence_frame_search(request_object['o'])
                )
        else:
            return Renders.index(request)
