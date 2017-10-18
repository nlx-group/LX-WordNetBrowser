"use strict";

function languageSettings(type, language) {
    const languageList = {
        'Portuguese': {
            'concept': 'conceitos relacionados',
            'relationsMenu': {
                'translation': 'traduções',
                'directHypernym': 'hiperónimos diretos',
                'inheritedHypernym': 'transitivos',
                'directHyponym': 'hipónimos diretos',
                'fullHyponym': 'transitivos',
                'directTroponym': 'tropónimos diretos',
                'fullTroponym': 'transitivos',
                'memberHolonym': 'holónimos (membros de coleção)',
                'substanceHolonym': 'holónimos (substâncias)',
                'partHolonym': 'holónimos (partes de)',
                'memberMeronym': 'merónimos (membros de coleção)',
                'substanceMeronym': 'merónimos (substâncias)',
                'partMeronym': 'merónimos (partes de)',
                'antonym': 'antônimo',
                'instanceHypernym': 'hiperónimos instância',
                'instanceHyponym': 'hipónimos instância',
                'attribute': 'atributo',
                'derivationallyRelatedForm': 'formas derivacionalmente relacionadas',
                'entailment': 'implicação',
                'cause': 'causa',
                'alsoSee': 'ver também',
                'verbGroup': 'grupo verbal',
                'similarTo': 'semelhante a',
                'participleOfVerb': 'particípio de verbo',
                'pertainym': 'concerne a',
                'derivedFromAdjective': 'derivado de adjetivo',
                'domainCategory': 'categoria de domínio',
                'domainTermCategory': 'termo de categoria de domínio',
                'domainRegion': 'categoria de região',
                'domainTermRegion': 'termo de categoria de região',
                'domainUsage': 'categoria de uso',
                'domainTermUsage': 'termo de categoria de uso',
                'noRelations': 'Este synset não tem relações registadas com qualquer outro',
                'derivationallyRelatedFormDisplay': 'Relacionado a:',
                'concept': 'conceito',
                'overview':'sinopse',
                'sentenceFrame': 'quadros de subcategorização frásicos'
            },
            'searchNotFound': 'A busca não encontrou a palavra que procura.',
            'defLabel': 'definição',
            'transConcept': 'conceito',
            'formLabel': 'traduzir para: ',
            'searchInput': 'pesquisar uma palavra',
            'search': 'pesquisa',
            'globe': 'traduções',
            'startPhrase': 'línguas: ',
            'languageChange': 'selecionar língua',
            'noTransLangSelected': 'nenhuma língua selecionada',
            'collision': 'A palavra que procura existe em várias línguas. Selecione no menu abaixo qual pretende ' +
            'explorar.'
        },
        'English': {
            'concept': 'related concepts',
            'relationsMenu': {
                'translation': 'translate',
                'directHypernym': 'direct ',
                'inheritedHypernym': 'transitive hypernyms',
                'directHyponym': 'direct ',
                'fullHyponym': 'transitive hyponyms',
                'directTroponym': 'direct ',
                'fullTroponym': 'transitive troponym',
                'memberHolonym': 'member holonyms',
                'substanceHolonym': 'substance holonyms',
                'partHolonym': 'part holonyms',
                'memberMeronym': 'member meronyms',
                'substanceMeronym': 'substance meronyms',
                'partMeronym': 'part meronym',
                'antonym': 'antonyms',
                'instanceHypernym': 'instance hypernyms',
                'instanceHyponym': 'instance hyponyms',
                'attribute': 'attribute',
                'derivationallyRelatedForm': 'derivationally related forms',
                'entailment': 'entailment',
                'cause': 'cause',
                'alsoSee': 'also see',
                'verbGroup': 'verb group',
                'similarTo': 'similar to',
                'participleOfVerb': 'participle of verb',
                'pertainym': 'pertainym',
                'derivedFromAdjective': 'derived from adjective',
                'domainCategory': 'domain category',
                'domainTermCategory': 'domain term category',
                'domainRegion': 'domain region',
                'domainTermRegion': 'domain term region',
                'domainUsage': 'domain usage',
                'domainTermUsage': 'domain term usage',
                'noRelations': 'This synset doesn\'t have any registered relations with any others',
                'derivationallyRelatedFormDisplay': 'Related to:',
                'concept': 'concept',
                'overview': 'overview',
                'sentenceFrame': 'sentence frames'
            },
            'searchNotFound': 'The search couldn\'t find the word you were looking for.',
            'defLabel': 'definition',
            'transConcept': 'concept',
            'formLabel': 'translations to: ',
            'searchInput': 'search for a word',
            'search': 'search',
            'globe': 'translations',
            'startPhrase': 'translations to: ',
            'languageChange': 'change the display language',
            'noTransLangSelected': 'no languages selected',
            'collision': 'The word you are searching for appears in more than one language. Choose which one you would'+
            ' like to explore through in the menu below.'
        }
    };
    return languageList[language][type];
}

function languageList(){
    return ['Suomi', 'Afrikaans', 'اللغة العربية الفصحى', 'Asturianu', 'Azərbaycan dili', '\tБеларуская мова','বাংলা', 'brezhoneg', '\tбългарски', 'català', 'čeština', 'Cymraeg', 'dansk', 'Deutsch', 'ελληνικά', 'Esperanto', 'eesti keel', 'euskara', 'Føroyskt','فارسى', 'Gàidhlig', 'Gaeilge', 'Galego', 'sɜːrboʊkroʊˈeɪʃən', 'עִבְרִית', 'हिन्दी', 'magyar', 'Bahasa Indonesia', 'Íslenska', 'italiano', '\t日本語', 'ქართული', '\t한국어', 'Lingua Latina', 'latviešu valoda', 'lietuvių kalba', 'македонски', 'Nederlands', 'Nynorsk', 'Bokmål', 'polski', 'român', 'Русский язык', 'slovenčina', 'slovenščina', 'español', 'Kiswahili', 'svenska', 'తెలుగు', 'ภาษาไทย', 'Türkçe', 'Українська', 'اردو', 'tiếng việt', 'Volapük', 'Bahasa melayu'];
}

function implementedLanguageList(){
    return ['Portuguese', 'English'];
}

function countryCodes(language) {
    const countryCodeList = {
        'Portuguese': {
            'en':'Inglês', 'fin':'Finlandês', 'afr':'Africâner', 'arb': 'Árabe','ast':'Asturiano','aze':'Azerbaijano',
            'bel':'Bielorusso','ben':'Bengali','bre':'Bretão','bul':'Búlgaro','cat':'Catalão','ces':'Tcheco',
            'cmn':'Chinês','cym':'Galês','dan':'Dinamarquês','deu':'Alemão','ell':'Grego','epo':'Esperanto',
            'est':'Estoniano','eus':'Basco','fao':'Feroês','fas':'Persa','fra':'Francês','gla':'Gaélico Escocês',
            'gle':'Irlandês','glg':'Galego','hbs':'Servo-Croata','heb':'Hebraico','hin':'Hindi','hun':'Húngaro',
            'ind':'Indonésio','isl':'Islandês','ita':'Italiano','jpn':'Japonês','kat':'Georgiano','kor':'Coreano',
            'lat':'Latim','lav':'Letão','lit':'Lituano','mkd':'Macedônio','nld':'Holandês','nno':'Novo Norueguês',
            'nob':'Bokmål Norueguês','pol':'Polaco','ron':'Romeno','rus':'Russo','slk':'Eslovaco','slv':'Esloveno',
            'spa':'Espanhol','swa':'Suaíli','swe':'Sueco','tel':'Telugu','tha':'Tailandês','tur':'Turco',
            'ukr':'Ucraniano','urd':'Urdu','vie':'Vietnamita','vol':'Volapuque','zsm':'Malaio'
        },
        'English': {
            'en':'English','fin':'Finnish','afr':'Afrikaans','arb':'Arabic','ast':'Asturian','aze':'Azerbaijani',
            'bel':'Belarusian','ben':'Bengali','bre':'Breton','bul':'Bulgarian','cat':'Catalan','ces':'Czech',
            'cmn':'Chinese','cym':'Welsh','dan':'Danish','deu':'German','ell':'Greek','epo':'Esperanto',
            'est':'Estonian','eus':'Basque','fao':'Faroese','fas':'Farsi','fra':'French','gla':'Scottish Gaelic',
            'gle':'Irish','glg':'Galician','hbs':'Serbo-Croatian','heb':'Hebrew','hin':'Hindi','hun':'Hungarian',
            'ind':'Indonesian','isl':'Icelandic','ita':'Italian','jpn':'Japanese','kat':'Georgian','kor':'Korean',
            'lat':'Latin','lav':'Latvian','lit':'Lithuanian','mkd':'Macedonian','nld':'Dutch','nno':'Nynorsk',
            'nob':'Bokmål','pol':'Polish','ron':'Romanian','rus':'Russian','slk':'Slovak','slv':'Slovene',
            'spa':'Spanish','swa':'Swahili','swe':'Swedish','tel':'Telugu','tha':'Thai','tur':'Turkish',
            'ukr':'Ukrainian','urd':'Urdu','vie':'Vietnamese','vol':'Volapük','zsm':'Malaysian'
        }
    };
    return countryCodeList[language]
}

function wikipediaLinkList(language) {
    const wikipediaList = {
        'English': {
            'en':'https://en.wikipedia.org/wiki/English_language',
            'fin':'https://en.wikipedia.org/wiki/Finnish_language','afr':'https://en.wikipedia.org/wiki/Afrikaans',
            'arb':'https://en.wikipedia.org/wiki/Arabic','ast':'https://en.wikipedia.org/wiki/Asturian_language',
            'aze':'https://en.wikipedia.org/wiki/Azerbaijani_language',
            'bel':'https://en.wikipedia.org/wiki/Belarusian_language',
            'ben':'https://en.wikipedia.org/wiki/Bengali_language','bre':'https://en.wikipedia.org/wiki/Breton_language'
            ,'bul':'https://en.wikipedia.org/wiki/Bulgarian_language',
            'cat':'https://en.wikipedia.org/wiki/Catalan_language',
            'ces':'https://en.wikipedia.org/wiki/Czech_language','cmn':'https://en.wikipedia.org/wiki/Chinese_language',
            'cym':'https://en.wikipedia.org/wiki/Welsh_language','dan':'https://en.wikipedia.org/wiki/Danish_language',
            'deu':'https://en.wikipedia.org/wiki/German_language','ell':'https://en.wikipedia.org/wiki/Greek_language',
            'epo':'https://en.wikipedia.org/wiki/Esperanto','est':'https://en.wikipedia.org/wiki/Estonian_language',
            'eus':'https://en.wikipedia.org/wiki/Basque_language','fao':'https://en.wikipedia.org/wiki/Faroese_language'
            ,'fas':'https://en.wikipedia.org/wiki/Persian_language','fra':'https://en.wikipedia.org/wiki/French_language'
            ,'gla':'https://en.wikipedia.org/wiki/Scottish_Gaelic','gle':'https://en.wikipedia.org/wiki/Irish_language',
            'glg':'https://en.wikipedia.org/wiki/Galician_language','hbs':'https://en.wikipedia.org/wiki/Serbo-Croatian'
            ,'heb':'https://en.wikipedia.org/wiki/Hebrew_language','hin':'https://en.wikipedia.org/wiki/Hindi',
            'hun':'https://en.wikipedia.org/wiki/Hungarian_language',
            'ind':'https://en.wikipedia.org/wiki/Indonesian_language',
            'isl':'https://en.wikipedia.org/wiki/Icelandic_language',
            'ita':'https://en.wikipedia.org/wiki/Italian_language',
            'jpn':'https://en.wikipedia.org/wiki/Japanese_language',
            'kat':'https://en.wikipedia.org/wiki/Georgian_language',
            'kor':'https://en.wikipedia.org/wiki/Korean_language','lat':'https://en.wikipedia.org/wiki/Latin',
            'lav':'https://en.wikipedia.org/wiki/Latvian_language',
            'lit':'https://en.wikipedia.org/wiki/Lithuanian_language',
            'mkd':'https://en.wikipedia.org/wiki/Macedonian_language',
            'nld':'https://en.wikipedia.org/wiki/Dutch_language','nno':'https://en.wikipedia.org/wiki/Nynorsk',
            'nob':'https://en.wikipedia.org/wiki/Bokmål','pol':'https://en.wikipedia.org/wiki/Polish_language',
            'ron':'https://en.wikipedia.org/wiki/Romanian_language',
            'rus':'https://en.wikipedia.org/wiki/Russian_language','slk':'https://en.wikipedia.org/wiki/Slovak_language'
            ,'slv':'https://en.wikipedia.org/wiki/Slovene_language',
            'spa':'https://en.wikipedia.org/wiki/Spanish_language',
            'swa':'https://en.wikipedia.org/wiki/Swahili_language',
            'swe':'https://en.wikipedia.org/wiki/Swedish_language','tel':'https://en.wikipedia.org/wiki/Telugu_language'
            ,'tha':'https://en.wikipedia.org/wiki/Thai_language','tur':'https://en.wikipedia.org/wiki/Turkish_language'
            ,'ukr':'https://en.wikipedia.org/wiki/Ukrainian_language','urd':'https://en.wikipedia.org/wiki/Urdu',
            'vie':'https://en.wikipedia.org/wiki/Vietnamese_language','vol':'https://en.wikipedia.org/wiki/Volapük',
            'zsm':'https://en.wikipedia.org/wiki/Malaysian_language'
        },
        'Portuguese': {
            'en':'https://pt.wikipedia.org/wiki/Língua_inglesa','fin':'https://pt.wikipedia.org/wiki/Língua_finlandesa',
            'afr':'https://pt.wikipedia.org/wiki/Língua_africâner','arb':'https://pt.wikipedia.org/wiki/Língua_árabe',
            'ast':'https://pt.wikipedia.org/wiki/Língua_asturiana','aze':'https://pt.wikipedia.org/wiki/Língua_azeri',
            'bel':'https://pt.wikipedia.org/wiki/Língua_bielorrussa',
            'ben':'https://pt.wikipedia.org/wiki/Língua_bengali','bre':'https://pt.wikipedia.org/wiki/Língua_bretã',
            'bul':'https://pt.wikipedia.org/wiki/Língua_búlgara','cat':'https://pt.wikipedia.org/wiki/Língua_catalã',
            'ces':'https://pt.wikipedia.org/wiki/Língua_tcheca','cmn':'https://pt.wikipedia.org/wiki/Língua_chinesa',
            'cym':'https://pt.wikipedia.org/wiki/Língua_galesa','dan':'https://pt.wikipedia.org/wiki/Língua_dinamarquesa'
            ,'deu':'https://pt.wikipedia.org/wiki/Língua_alemã','ell':'https://pt.wikipedia.org/wiki/Língua_grega',
            'epo':'https://pt.wikipedia.org/wiki/Língua_esperanto','est':'https://pt.wikipedia.org/wiki/Língua_estónia',
            'eus':'https://pt.wikipedia.org/wiki/Língua_basca','fao':'https://pt.wikipedia.org/wiki/Língua_feroesa',
            'fas':'https://pt.wikipedia.org/wiki/Língua_persa','fra':'https://pt.wikipedia.org/wiki/Língua_francesa',
            'gla':'https://pt.wikipedia.org/wiki/Língua_gaélica_escocesa',
            'gle':'https://pt.wikipedia.org/wiki/Língua_irlandesa','glg':'https://pt.wikipedia.org/wiki/Língua_galega',
            'hbs':'https://pt.wikipedia.org/wiki/Língua_servo-croata',
            'heb':'https://pt.wikipedia.org/wiki/Língua_hebraica','hin':'https://pt.wikipedia.org/wiki/Língua_hindi',
            'hun':'https://pt.wikipedia.org/wiki/Língua_húngara','ind':'https://pt.wikipedia.org/wiki/Língua_indonésia',
            'isl':'https://pt.wikipedia.org/wiki/Língua_islandesa','ita':'https://pt.wikipedia.org/wiki/Língua_italiana',
            'jpn':'https://pt.wikipedia.org/wiki/Língua_japonesa','kat':'https://pt.wikipedia.org/wiki/Língua_georgiana',
            'kor':'https://pt.wikipedia.org/wiki/Língua_coreana','lat':'https://pt.wikipedia.org/wiki/Latim',
            'lav':'https://pt.wikipedia.org/wiki/Língua_letã','lit':'https://pt.wikipedia.org/wiki/Língua_lituana',
            'mkd':'https://pt.wikipedia.org/wiki/Língua_macedônia',
            'nld':'https://pt.wikipedia.org/wiki/Língua_neerlandesa',
            'nno':'https://pt.wikipedia.org/wiki/Língua_nova_norueguesa',
            'nob':'https://pt.wikipedia.org/wiki/Língua_bokmål_norueguesa',
            'pol':'https://pt.wikipedia.org/wiki/Língua_polaca','ron':'https://pt.wikipedia.org/wiki/Língua_romena',
            'rus':'https://pt.wikipedia.org/wiki/Língua_russa','slk':'https://pt.wikipedia.org/wiki/Língua_eslovaca',
            'slv':'https://pt.wikipedia.org/wiki/Língua_eslovena',
            'spa':'https://pt.wikipedia.org/wiki/Língua_castelhana','swa':'https://pt.wikipedia.org/wiki/Língua_suaíli',
            'swe':'https://pt.wikipedia.org/wiki/Língua_sueca','tel':'https://pt.wikipedia.org/wiki/Língua_telugo',
            'tha':'https://pt.wikipedia.org/wiki/Língua_tailandesa','tur':'https://pt.wikipedia.org/wiki/Língua_turca',
            'ukr':'https://pt.wikipedia.org/wiki/Língua_ucraniana','urd':'https://pt.wikipedia.org/wiki/Língua_urdu',
            'vie':'https://pt.wikipedia.org/wiki/Língua_vietnamita','vol':'https://pt.wikipedia.org/wiki/Volapuque',
            'zsm':'https://en.wikipedia.org/wiki/Malaysian_language'
        }
    };
    return wikipediaList[language];
}

function partOfSpeechList(language) {
    const posList = {
        'Portuguese': {
            'Noun': 'Substantivo',
            'Adj': 'Adjetivo',
            'Verb': 'Verbo',
            'Adv': 'Advérbio'
        },
        'English': {
            'Noun': 'Noun',
            'Adj': 'Adjective',
            'Verb': 'Verb',
            'Adv': 'Adverb'
        }
    };
    return posList[language];
}