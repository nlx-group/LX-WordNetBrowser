from django.http import JsonResponse
from django.shortcuts import render
import json
import os
import logging
from datetime import datetime, timedelta

pointer_map = {'Hypernym': '@', 'Hyponym': '~', 'Member_Holonym': '#m', 'Substance_Holonym': '#s', 'Part_Holonym': '#p',
               'Member_Meronym': r'%m', 'Substance_Meronym': r'%s', 'Part_Meronym': r'%p', 'Antonym': '!',
               'Instance_Hypernym': '@i', 'Instance_Hyponym': '~i', 'Attribute': '=',
               'Derivationally_related_form': '+',
               'Entailment': '*', 'Cause': '>', 'Also_see': '^', 'Verb_Group': '$', 'Similar_to': '&',
               'Participle_of_verb': '<',
               'Pertainym': '\\'}

pointer_name_map = {'ihype': 'Hypernym', 'dhype': 'Hypernym', 'fhypo': 'Hyponym', 'dhypo': 'Hyponym',
                    'mh': 'Member_Holonym',
                    'sh': 'Substance_Holonym', 'ph': 'Part_Holonym', 'mm': 'Member_Meronym', 'sm': 'Substance_Meronym',
                    'pm': 'Part_Meronym', 'ant': 'Antonym', 'inhype': 'Instance_Hypernym', 'inhypo': 'Instance_Hyponym',
                    'attr': 'Attribute', 'derform': 'Derivationally_related_form', 'ent': 'Entailment', 'ca': 'Cause',
                    'asee': 'Also_see', 'vgr': 'Verb_Group', 'sto': 'Similar_to', 'pverb': 'Participle_of_verb',
                    'per': 'Pertainym'}

part_of_speech = {'n': 'noun', 'v': 'verb', 'a': 'adj', 's': 'adj', 'r': 'adv'}

main_language = 'English'   # Set the main language here
link_file_path = None        # If not using English as a main language and want to use a custom tab link file,
pivot_language = 'English'  # set its path here


class FileCheck:
    @staticmethod
    def check_files():
        files = os.listdir(os.path.join(os.curdir, 'langdata', 'main'))
        files_present = []
        for file in files:
            extension = os.path.splitext(file)[1][1:]
            name = os.path.splitext(file)[0]
            if (name == 'data' or name == 'index') and extension != 'sense' and extension not in files_present:
                files_present.append(extension)
        return files_present


class Parsers:
    @staticmethod
    def line_parser(line, offset):
        """
        Creates an HTML line for the synset display.

        Requires: line is a string, offset is a string
        Ensures: A string that is in HTML form, ready to be displayed.
        """
        return '<li class="' + offset + '-' + line[2] + '"><a class="concept" data-tool-tip="tooltip" style="cursor:pointer">rels </a> <span style="color:red">(' + \
               line[2] + ')</span>' + ''.join(
            [' ' + '<span class="mark">' + name.replace('_', ' ') + '</span>' + ',' for name in
             line[4:4 + int(line[3], 16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + line[
                   4 + int(line[3], 16) * 2 - 2].replace('_', ' ') + '</span>'


class SearchRoutines:
    def __init__(self, offset):
        self.offset_holder = offset

    def full_search(self, file_types, pos, offset, search_type, depth, max_depth=None, max_length=None):
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
        with open(os.path.join(os.curdir, 'langdata', 'main', 'data.' + part_of_speech[pos])) as file_reader:
            file_reader.seek(int(offset), 0)
            offset_line = file_reader.readline()
            split_line = offset_line.split()
            relations_offset = []
            for i in range(5 + int(split_line[3], 16) * 2,
                           5 + int(split_line[3], 16) * 2 + int(split_line[4 + int(split_line[3], 16) * 2]) * 4, 4):
                if split_line[i] == pointer:
                    relations_offset.append(split_line[i + 1])
                if split_line[0] not in relations:
                    relations[split_line[0]] = [split_line[i]]
                else:
                    if split_line[i] not in relations[split_line[0]]:
                        relations[split_line[0]].append(split_line[i])
            max_local_length = 0
            if max_length is not None:
                max_local_length = (len(relations_offset) if max_length > len(relations_offset) else max_length)
            else:
                max_local_length = len(relations_offset)
            if max_depth == None:
                if len(relations_offset) > 0:
                    for _ in range(max_local_length):
                        if first and offset != self.offset_holder:
                            line += '<ul>' + Parsers.line_parser(split_line, split_line[0])
                            first = False
                        result = self.full_search(file_types, pos, relations_offset[idnum2], search_type, str(int(depth) + 1),
                                                  max_depth,
                                                  max_local_length)
                        relations.update(result['relations'])
                        line += result['line'] + '</li>'
                        idnum2 += 1
                    return {'relations': relations, 'line': line + '</ul>'}
                else:
                    if split_line[0] not in relations:
                        relations[split_line[0]] = []
                    line += '<ul>' + Parsers.line_parser(split_line, split_line[0])
                    return {'line': line + '</li></ul>', 'relations': relations}
            else:
                if int(depth) < max_depth:
                    if first and offset != self.offset_holder:
                        line += '<ul>' + Parsers.line_parser(split_line, split_line[0])
                        first = False
                    for _ in range(max_local_length):
                        result = self.full_search(file_types, pos, relations_offset[idnum2], search_type, str(int(depth) + 1), max_depth,
                                                  max_local_length)
                        relations.update(result['relations'])
                        line += result['line'] + '</li>'
                        idnum2 += 1
                    if split_line[0] not in relations:
                        relations[split_line[0]] = []
                    return {'relations': relations, 'line': line + '</ul>'}
                else:
                    return {'relations': relations, 'line': line}

    def expand_search(self, file_types, pos, offset, search_type):
        """
        Redirects the search to their appropriate functions, depending on whether it is a direct sibling search or full
        tree search.

        Requires: Offset is an int, search_type, idnum and depth are strings.
        Ensures: A dictionary resulting from the called function.
        """
        self.offset_holder = offset
        if search_type != 'fhypo' and search_type != 'ihype':
            result = self.full_search(file_types, pos, offset, search_type, 0, 2)
            return {'relations': {part_of_speech[pos]: result['relations']}, 'line': result['line']}
        else:
            if search_type == 'ihype':
                result = self.full_search(file_types, pos, offset, search_type, 0)
                return {'relations': {part_of_speech[pos]: result['relations']}, 'line': result['line']}
            else:
                result = self.full_search(file_types, pos, offset, search_type, 0, 4, 10)
                return {'relations': {part_of_speech[pos]: result['relations']}, 'line': result['line']}

    @staticmethod
    def normal_search(file_types, lemma):
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
        for file in file_types:
            with open(os.path.join(os.curdir, 'langdata', 'main', 'index.' + file)) as file_reader:
                for line in file_reader:
                    if line.split()[0] == lemma:
                        index_line = line
                        break
            if index_line:
                offsets = index_line.split()[3 + int(index_line.split()[3]) + 3:]
                with open(os.path.join(os.curdir, 'langdata', 'main', 'data.' + file)) as file_reader:
                    for offset in offsets:
                        file_reader.seek(int(offset), 0)
                        data_lines.append(file_reader.readline())
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
                        0] + '-' + split_line[2] + '"><a class="concept" data-tool-tip="tooltip" style="cursor:pointer">rels </a> <span style="color:red">(' + \
                                 split_line[2] + ')</span>' + ''.join(
                        [' ' + '<span class="mark">' + name.replace('_', ' ') + '</span>' + ',' for name in
                         split_line[4:4 + int(split_line[3], 16) * 2 - 2:2]]) + ' ' + '<span class="mark">' + split_line[
                                     4 + int(split_line[3], 16) * 2 - 2].replace('_', ' ') + '</span>' + '</li>'
                result['line'] += '<h2>' + file[0].upper() + file[1:] + '</h2>' + html_line
                result['relations'][(file if file != 's' else 'adj')] = relations
                result['found'] = 1
                index_line = ''
                data_lines = []
                html_line = ''
                relations = {}
        if not result['line']:
            return {'line': ["<p> The search couldn't find the word you were looking for. </p>"], 'found': 0}
        return result

    @staticmethod
    def advanced_search(offset, langs, pos):
        languages = json.loads(langs)
        pivot_language_offset = (offset if main_language == 'English' and pivot_language == 'English' else '')
        html_lines = {}
        if main_language == 'Portuguese':
            with open(link_file_path) as file_reader:
                for line in file_reader:
                    if line.split()[0] == offset:
                        pivot_language_offset = line.split()[1][3:]
                        break
        # Method here to obtain pivot language offset if wordnet != Portuguese
        for language in languages:
            html_lines[language] = {'lemma': '', 'def': ''}
            if language == 'en' and pivot_language == 'English':
                with open(os.path.join(os.curdir, 'langdata', 'dict', 'data.' + part_of_speech[pos])) as data_file:
                    data_file.seek(int(pivot_language_offset), 0)
                    line = data_file.readline()
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
                with open(os.path.join(os.curdir, 'langdata', 'tab files', 'wn-wikt-' + language + '.tab')) as data_file:
                    for line in data_file:
                        if line.split()[0] == pivot_language_offset + '-' + pos:
                            if line.split()[1].split(':')[1] == 'lemma':
                                if html_lines[language]['lemma'] != '':
                                    html_lines[language]['lemma'] += ', ' + line.split()[2]
                                else:
                                    html_lines[language]['lemma'] += line.split()[2]
                            elif 'def' in line.split()[1].split(':')[1]:
                                html_lines[language]['def'] += ' ' + line.split()[2]
                            break

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


class BotCheck:
    @staticmethod
    def check_connection_number(IP, max_connections, delta_time, line_size=42):
        """
        """
        num_connections = 0
        access_time = datetime.now()
        with open('access.log', 'a+') as access_file:
            access_line = IP + ',' + access_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            access_file.write(
                access_line + (',' * (line_size - len(access_line)) if len(access_line) < line_size else '') + '\n')
            time_delta = timedelta(seconds=delta_time)
            access_file.seek(0, 2)
            file_size = access_file.tell()
            current_offset = file_size
            flag = False
            while current_offset > 0 and not flag:
                access_file.seek(current_offset - line_size - 1, 0)
                line = access_file.readline()
                log_time = datetime.strptime(line.split(',')[1].strip('\n'), '%Y-%m-%d %H:%M:%S.%f')
                if access_time - time_delta <= log_time and log_time <= access_time:
                    if line.split(',')[0] == IP:
                        num_connections += 1
                else:
                    flag = True
                current_offset -= line_size + 1
        return False if num_connections > max_connections else True


class Initializer:
    @staticmethod
    def init(request):
        """
        Treats the request and redirects the query to their appropriate functions.
        """
        blacklist = ''
        whitelist = ''
        client_IP = request.META['REMOTE_ADDR']
        with open('blacklist.txt') as blacklist_file:
            blacklist = blacklist_file.read()
        with open('whitelist.txt') as whitelist_file:
            whitelist = whitelist_file.read()
        if client_IP not in blacklist:
            if client_IP not in whitelist:
                if BotCheck.check_connection_number(client_IP, 1000, 10):  # Tweak connections here
                    if request.method == 'GET' and request.is_ajax():
                        file_types = FileCheck.check_files()
                        request_object = request.GET
                        if len(request_object) == 1:
                            return JsonResponse(SearchRoutines.normal_search(file_types, request_object['s']))
                        elif len(request_object) == 3:
                            return JsonResponse(
                                SearchRoutines(None).advanced_search(request_object['o'], request_object['langs'],
                                                                     request_object['c']))
                        elif len(request_object) == 4:
                            return JsonResponse(
                                SearchRoutines(None).expand_search(file_types, request_object['c'], request_object['o']
                                                                   , request_object['t']))
                    else:
                        return Renders.index(request)
                else:
                    with open('blacklist.txt', 'a') as blacklist_file:
                        blacklist_file.write(client_IP + '\n')
            else:
                if request.method == 'GET' and request.is_ajax():
                    file_types = FileCheck.check_files()
                    request_object = request.GET
                    if len(request_object) == 1:
                        return JsonResponse(SearchRoutines.normal_search(file_types, request_object['s']))
                    elif len(request_object) == 3:
                        return JsonResponse(
                            SearchRoutines(None).advanced_search(request_object['o'], request_object['langs'],
                                                                 request_object['c']))
                    elif len(request_object) == 4:
                        return JsonResponse(
                            SearchRoutines(None).expand_search(file_types, request_object['c'], request_object['o'],
                                                               request_object['t']))
                else:
                    return Renders.index(request)
