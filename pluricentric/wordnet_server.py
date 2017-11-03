#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
import argparse
import logging
import os


class WordNet:
    def __init__(self, browser_path, browser_type):
        self.browser_path = browser_path
        self.browser_type = browser_type
        self.wordnet_content = self.wordnet_loader()
        self.tab_content = self.tab_loader()

    def wordnet_loader(self):
        if self.browser_type == 'pluricentric':
            wordnet_content = {}
            languages = os.listdir(os.path.join(self.browser_path, 'langdata', 'wordnets'))
            for language in languages:
                if language[0] != '.':
                    wordnet_content[language] = {}
                    files_present = self.check_file_types(os.listdir(os.path.join(self.browser_path, 'langdata', 'wordnets', language)))
                    for file in files_present:
                        wordnet_content[language][file] = {}
                        if file != 'vrb':
                            with open(os.path.join(self.browser_path, 'langdata', 'wordnets', language, 'index.' + file)) as file_reader:
                                wordnet_content[language][file]['index'] = {}
                                for line in file_reader:
                                    if line[0] != '#' and line[0] != ' ':
                                        wordnet_content[language][file]['index'][line.split()[0]] = line.rstrip('\n')
                            with open(os.path.join(self.browser_path, 'langdata', 'wordnets', language, 'data.' + file)) as file_reader:
                                wordnet_content[language][file]['data'] = {}
                                for line in file_reader:
                                    if line[0] != '#' and line[0] != ' ':
                                        wordnet_content[language][file]['data'][line.split()[0]] = line.rstrip('\n')
                        else:
                            files = os.listdir(os.path.join(self.browser_path, 'langdata', 'wordnets', language))
                            if 'sentidx.vrb' in files:
                                wordnet_content[language][file]['sentidx'] = {}
                                with open(os.path.join(self.browser_path, 'langdata', 'wordnets', language, 'sentidx.vrb')) as file_reader:
                                    for line in file_reader:
                                        wordnet_content[language][file]['sentidx'][line.split('%')[0]] = line.rstrip('\n')
                            if 'sents.vrb' in files:
                                wordnet_content[language][file]['sents'] = {}
                                with open(os.path.join(self.browser_path, 'langdata', 'wordnets', language, 'sents.vrb')) as file_reader:
                                    for line in file_reader:
                                        wordnet_content[language][file]['sents'][line.split()[0]] = line.rstrip('\n')
                            if 'frames.vrb' in files:
                                wordnet_content[language][file]['frames'] = {}
                                with open(os.path.join(self.browser_path, 'langdata', 'wordnets', language, 'frames.vrb')) as file_reader:
                                    for line in file_reader:
                                        wordnet_content[language][file]['frames'][line.split()[0]] = line.rstrip('\n')
            print('WordNet content loaded')
            logging.info('WordNet content loaded')
            return wordnet_content
        else:
            wordnet_content = {}
            # main language
            files_present_main = self.check_file_types(
                os.listdir(os.path.join(self.browser_path, 'langdata', 'main')))
            wordnet_content['main'] = {}
            for file in files_present_main:
                wordnet_content['main'][file] = {}
                if file != 'vrb':
                    with open(os.path.join(self.browser_path, 'langdata', 'main',
                                           'index.' + file)) as file_reader:
                        wordnet_content['main'][file]['index'] = {}
                        for line in file_reader:
                            if line[0] != '#' and line[0] != ' ':
                                wordnet_content['main'][file]['index'][line.split()[0]] = line.rstrip('\n')
                    with open(os.path.join(self.browser_path, 'langdata', 'main',
                                           'data.' + file)) as file_reader:
                        wordnet_content['main'][file]['data'] = {}
                        for line in file_reader:
                            if line[0] != '#' and line[0] != ' ':
                                wordnet_content['main'][file]['data'][line.split()[0]] = line.rstrip('\n')
                else:
                    files = os.listdir(os.path.join(self.browser_path, 'langdata', 'main'))
                    if 'sentidx.vrb' in files:
                        wordnet_content['main'][file]['sentidx'] = {}
                        with open(os.path.join(self.browser_path, 'langdata', 'main',
                                               'sentidx.vrb')) as file_reader:
                            for line in file_reader:
                                wordnet_content['main'][file]['sentidx'][line.split('%')[0]] = line.rstrip('\n')
                    if 'sents.vrb' in files:
                        wordnet_content['main'][file]['sents'] = {}
                        with open(os.path.join(self.browser_path, 'langdata', 'main',
                                               'sents.vrb')) as file_reader:
                            for line in file_reader:
                                wordnet_content['main'][file]['sents'][line.split()[0]] = line.rstrip('\n')
                    if 'frames.vrb' in files:
                        wordnet_content['main'][file]['frames'] = {}
                        with open(os.path.join(self.browser_path, 'langdata', 'main',
                                               'frames.vrb')) as file_reader:
                            for line in file_reader:
                                wordnet_content['main'][file]['frames'][line.split()[0]] = line.rstrip('\n')
            # pivot
            files_present_pivot = self.check_file_types(
                os.listdir(os.path.join(self.browser_path, 'langdata', 'pivot')))
            wordnet_content['pivot'] = {}
            for file in files_present_pivot:
                wordnet_content['pivot'][file] = {}
                if file != 'vrb':
                    with open(os.path.join(self.browser_path, 'langdata', 'pivot',
                                           'index.' + file)) as file_reader:
                        wordnet_content['pivot'][file]['index'] = {}
                        for line in file_reader:
                            if line[0] != '#' and line[0] != ' ':
                                wordnet_content['pivot'][file]['index'][line.split()[0]] = line.rstrip('\n')
                    with open(os.path.join(self.browser_path, 'langdata', 'pivot',
                                           'data.' + file)) as file_reader:
                        wordnet_content['pivot'][file]['data'] = {}
                        for line in file_reader:
                            if line[0] != '#' and line[0] != ' ':
                                wordnet_content['pivot'][file]['data'][line.split()[0]] = line.rstrip('\n')
                else:
                    files = os.listdir(os.path.join(self.browser_path, 'langdata', 'pivot'))
                    if 'sentidx.vrb' in files:
                        wordnet_content['pivot'][file]['sentidx'] = {}
                        with open(os.path.join(self.browser_path, 'langdata', 'pivot',
                                               'sentidx.vrb')) as file_reader:
                            for line in file_reader:
                                wordnet_content['pivot'][file]['sentidx'][line.split('%')[0]] = line.rstrip('\n')
                    if 'sents.vrb' in files:
                        wordnet_content['pivot'][file]['sents'] = {}
                        with open(os.path.join(self.browser_path, 'langdata', 'pivot',
                                               'sents.vrb')) as file_reader:
                            for line in file_reader:
                                wordnet_content['pivot'][file]['sents'][line.split()[0]] = line.rstrip('\n')
                    if 'frames.vrb' in files:
                        wordnet_content['pivot'][file]['frames'] = {}
                        with open(os.path.join(self.browser_path, 'langdata', 'pivot',
                                               'frames.vrb')) as file_reader:
                            for line in file_reader:
                                wordnet_content['pivot'][file]['frames'][line.split()[0]] = line.rstrip('\n')
            print('WordNet content loaded')
            logging.info("WordNet content loaded")
            return wordnet_content

    def tab_loader(self):
        tab_content = {}
        for file in os.listdir(os.path.join(self.browser_path, 'langdata', 'tab files')):
            if file[0] != '.':
                language_code = file.split('.')[0].split('-')[-1]
                tab_content[language_code] = {}
                with open(os.path.join(self.browser_path, 'langdata', 'tab files', file)) as file_reader:
                    for line in file_reader:
                        tab_content[language_code][line.split()[0]] = line.rstrip('\n')
        print('Tab content loaded')
        return tab_content

    def get_index(self, language, pos, lemma):
        if pos in self.wordnet_content[language]:
            if lemma in self.wordnet_content[language][pos]['index']:
                return self.wordnet_content[language][pos]['index'][lemma]
        return None

    def get_data(self, language, pos, offset):
        if pos in self.wordnet_content[language]:
            return self.wordnet_content[language][pos]['data'][offset]
        return None

    def get_sentidx(self, language, verb):
        if 'sentidx' in self.wordnet_content[language]['vrb']:
            if verb in self.wordnet_content[language]['vrb']['sentidx']:
                return self.wordnet_content[language]['vrb']['sentidx'][verb]
        return None

    def get_sents(self, language, number):
        if 'sents' in self.wordnet_content[language]['vrb']:
            return self.wordnet_content[language]['vrb']['sents'][number]
        return None

    def get_frame(self, language, number):
        if 'frames' in self.wordnet_content[language]['vrb']:
            return self.wordnet_content[language]['vrb']['frames'][number]
        return None

    def get_tab(self, language, offset, pos):
        if language in self.tab_content:
            if offset + '-' + pos in self.tab_content[language]:
                return self.tab_content[language][offset + '-' + pos]
        return None

    def get_whole_tab(self, language):
        if language in self.tab_content:
            return self.tab_content[language]
        return None

    def pos_available(self, language):
        return list(self.wordnet_content[language].keys())

    def languages_available(self):
        return list(self.wordnet_content.keys())

    @staticmethod
    def check_file_types(files):
        files_present = []
        for file in files:
            extension = os.path.splitext(file)[1][1:]
            name = os.path.splitext(file)[0]
            if name in ['data', 'index', 'sentidx', 'sents'] and extension != 'sense' and extension not in files_present:
                files_present.append(extension)
        return files_present


if __name__ == '__main__':
    description = "XML-RPC server that loads and supplies wordnet content for LX Wordnet Browser"
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument('port', metavar='PORT', type=int, help='listen on PORT')
    parser.add_argument('browser_path', metavar="browser_path", type=str, help="Path to wordnet browser location")
    parser.add_argument('browser_type', metavar='browser_type', type=str, help="Type of browser: pluricentric or basic")
    args = vars(parser.parse_args())
    try:
        wordnet = WordNet(args['browser_path'], args['browser_type'])
        server = SimpleXMLRPCServer(('127.0.0.1', args['port']), allow_none=True)
        server.register_introspection_functions()
        server.register_instance(wordnet)
        server.serve_forever()
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s:%(message)s')
    except KeyboardInterrupt:
        logging.info('keyboard interrupt received: stopping server')
