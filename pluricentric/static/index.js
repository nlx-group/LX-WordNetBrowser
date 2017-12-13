"use strict";
var currentSearchTerm;
var info = {};
var otherLangs = [];
var currentTranslatedOffset;
const relationsShort = {'DirectHypernym': 'dhype', 'DirectHyponym': 'dhypo', 'DirectTroponym': 'dhypo', 'InheritedHypernym':'ihype', 'FullHyponym': 'fhypo', 'FullTroponym': 'fhypo', 'MemberHolonym': 'mh', 'SubstanceHolonym': 'sh', 'PartHolonym': 'ph', 'MemberMeronym': 'mm', 'SubstanceMeronym': 'sm', 'PartMeronym': 'pm', 'Antonym': 'ant', 'InstanceHypernym': 'inhype', 'InstanceHyponym': 'inhypo', 'Attribute': 'attr', 'DerivationallyRelatedForm': 'derform', 'Entailment': 'ent', 'Cause': 'ca', 'AlsoSee': 'asee', 'VerbGroup': 'vgr', 'SimilarTo': 'sto', 'ParticipleOfVerb': 'pverb', 'Pertainym': 'per', 'DomainCategory': 'domcat', 'DomainTermCategory': 'domtermcat', 'DomainRegion': 'domreg', 'DomainTermRegion': 'domtermreg', 'DomainUsage': 'domusage', 'DomainTermUsage': 'domtermusage', 'Overview': 'ov', 'Concept':'con', 'SentenceFrame': 'sframe'};
const partOfSpeech = {'n': 'noun', 'v': 'verb', 'a': 'adj', 's': 'adj', 'r': 'adv'};
const nodeText = 'NODE: University of Lisbon';
var currentSearchLanguage;
var searchLangCache;


/**
 * Formats and appends data retrieved from an AJAX request to the server for relation searches
 * @param data is an object
 * @param event is an event object
 * @param remove is a boolean
 */
function expandedSearchFormatter(data,event,remove) {
	// save relations information from data
	for (var elem in data.relations) {
		for (var element in data.relations[elem]) {
			if (!info.hasOwnProperty(elem)) {
				info[elem] = {};
			}
			if (!info[elem].hasOwnProperty(element)) {
				info[elem][element] = data.relations[elem][element];
			}
		}
	}
	var language = localStorage.getItem('language');
	if (remove) {
		// Remove to override previous result
		$(event.target.parentNode.children[2]).remove();
	}
	// Append the results
	$(event.target.parentNode).append('<ul>' + data.line + '</ul>');
	// Differentiate between search types as there are different indices depending on them
	if (event.target.className === 'DirectHypernym' || event.target.className === 'DirectHyponym' || event.target.className === 'InheritedHypernym' || event.target.className === 'FullHyponym' || event.target.className === 'DirectTroponym' || event.target.className == 'FullTroponym') {
		$(event.target.parentNode.children[2]).find('a').click(function(event){expand(event)});
		// the line comes with the names with a class 'mark' so as to substitute them with a link
		$("span.mark").each(function() {
			var lemma = $(this).text();
			$(this).replaceWith('<a style="color:black;font-weight:bold;" href="http://' + location.hostname + ':' + location.port + '/search/s=' + lemma +'&search=normal">' + lemma + '</a>');
		});
		$(event.target.parentNode.children[2]).addClass(event.target.className+' search');
		$(event.target.parentNode.children[2]).find("ul").addClass('search');
	}
	else {
		$(event.target.parentNode.children[1]).find('a').click(function(event){expand(event)});
		$("span.mark").each(function() {
			var lemma = $(this).text();
			$(this).replaceWith('<a style="color:black;font-weight:bold;" href="http://' + location.hostname + ':' + location.port + '/search/s=' + lemma +'&search=normal">' + lemma + '</a>');
		});
		if (event.target.className === 'DerivationallyRelatedForm') {
			var relationsMenu = languageSettings('relationsMenu', language);
			// translation for a menu line
			$("span.derformMark").each(function() {
				$(this).replaceWith(relationsMenu['derivationallyRelatedFormDisplay']);
			});
		}
		$(event.target.parentNode.children[1]).addClass(event.target.className + ' search');
		$(event.target.parentNode.children[1]).find("ul").addClass('search');
	}
	// tooltip
	$(".concept").prop('title', languageSettings('concept', language));
	$('[data-tool-tip=tooltip]').tooltip({trigger:'hover', container:'body'});
}

/**
 * Appends the result from a sentence frame search
 * @param data is an object
 * @param event is an event object
 */
function sentenceFrameFormatter(data, event) {
	$(event.target.parentNode).append(data.line);
}

/**
 * Sends a AJAX request to the server to retrieve information upon a relation search from the expanded menu
 * @param event is an event object
 * @param remove is a boolean
 */
function expandRequest(event, remove=false) {
	var searchTypeParsed = relationsShort[event.target.className];
	var className = $(event.target.parentNode).parent().parent().prop('class');
	var offset = className.slice(0, className.length - 2);
	var pos = className[className.length - 1];
	if (searchTypeParsed === 'ov') {
		var searchTerm = $(event.target.parentNode).parent().parent().find('a')[1].textContent.trim();
		history.pushState(null, null, '/search/s=' + searchTerm + '&t=' + searchTypeParsed + '&language=' + currentSearchLanguage);
		$.ajax({type:'GET',url:'.', data:'s=' + searchTerm + '&t=' + searchTypeParsed + '&st=norm2' + '&language=' + currentSearchLanguage}).done(function(data){expandedSearchFormatter(data, event, remove)});
	}
	else if (searchTypeParsed === 'sframe') {
		history.pushState(null, null, '/search/s=' + currentSearchTerm + '&t=' + searchTypeParsed + '&o=' + offset + '&c=' + pos + '&language=' + currentSearchLanguage);
		$.ajax({type:'GET', url:'.', data:'s=' + currentSearchTerm + '&t=' + searchTypeParsed + '&o=' + offset + '&st=stframe' + '&language=' + currentSearchLanguage}).done(function(data){sentenceFrameFormatter(data, event)});
	}
	else {
		history.pushState(null, null,'/search/s=' + currentSearchTerm + '&o=' + offset + '&t=' + searchTypeParsed + '&c=' + pos + '&language=' + currentSearchLanguage);
		$.ajax({type:'GET',url:'.', data:'s='+ currentSearchTerm + '&o=' + offset + '&t=' + searchTypeParsed + '&c=' + pos + '&st=exp' + '&language=' + currentSearchLanguage}).done(function(data){expandedSearchFormatter(data, event, remove)});
	}
}

function expandedSearch(event) {
	if (event.target.className !== 'otherLangSearch') {
		if ($(event.target.parentNode).find("ul.search").length !== 0) {
			if (event.target.className === 'DirectHypernym' || event.target.className === 'InheritedHypernym' || event.target.className === 'DirectHyponym' || event.target.className === 'FullHyponym' || event.target.className === 'DirectTroponym' || event.target.className == 'FullTroponym') {
				if ($(event.target.parentNode.children[2]).prop("class") !== event.target.className + ' search') {
					expandRequest(event, true);
				}
				else {
					$(event.target.parentNode.children[2]).fadeToggle('slow');
				}
			}
			else {

				$(event.target.parentNode.children[1]).fadeToggle('slow');
			}
		}
		else {
			expandRequest(event);
		}
	}
	else {
		advancedSearchLangs(event);
	}
}

/**
 * Checks whether the search request is valid (or if the results should be hidden)
 * @param event is an event object
 */
function expand(event) {
	if ($(event.target.parentNode).find("ul.expand").length === 0) {
		var list = '';
		var pos = event.target.parentNode.className[event.target.parentNode.className.length - 1];
		var offset = event.target.parentNode.className.slice(0, event.target.parentNode.className.length - 2);
		var relations = info[partOfSpeech[pos]][offset];
		var id = String($("ul.expand").length);
		var relationsMenu = languageSettings('relationsMenu', localStorage.getItem('language'));
		var relationsMenuLines = {'@': '<li><a class="DirectHypernym" style="cursor:pointer">' + relationsMenu['directHypernym'] + '</a> | <a class="InheritedHypernym" style="cursor:pointer">' + relationsMenu['inheritedHypernym'] + '</a></li>',
			'~': ['<li><a class="DirectHyponym" style="cursor:pointer">' + relationsMenu['directHyponym'] + '</a> | <a class="FullHyponym" style="cursor:pointer">' + relationsMenu['fullHyponym'] + '</a></li>',
			'<li><a class="DirectTroponym" style="cursor:pointer">' + relationsMenu['directTroponym'] + '</a> | <a class="FullTroponym" style="cursor:pointer">' + relationsMenu['fullTroponym'] + '</a></li>'],
			'#m': '<li><a class="MemberHolonym" style="cursor:pointer">' + relationsMenu['memberHolonym'] + '</a></li>', '#s': '<li><a class="SubstanceHolonym" style="cursor:pointer">' + relationsMenu['substanceHolonym'] + '</a></li>',
			'#p': '<li><a class="PartHolonym" style="cursor:pointer">' + relationsMenu['partHolonym'] + '</a></li>', '%m': '<li><a class="MemberMeronym" style="cursor:pointer">' + relationsMenu['memberMeronym'] + '</a></li>',
			'%s': '<li><a class="SubstanceMeronym" style="cursor:pointer">' + relationsMenu['substanceMeronym'] + '</a></li>', '%p': '<li><a class="PartMeronym" style="cursor:pointer">' + relationsMenu['partMeronym'] + '</a></li>',
			'!': '<li><a class="Antonym" style="cursor:pointer">' + relationsMenu['antonym'] + '</a></li>', '@i': '<li><a class="InstanceHypernym" style="cursor:pointer">' + relationsMenu['instanceHypernym'] + '</a></li>',
			'~i': '<li><a class="InstanceHyponym" style="cursor:pointer">' + relationsMenu['instanceHyponym'] + '</a></li>', '=': '<li><a class="Attribute" style="cursor:pointer">' + relationsMenu['attribute'] + '</a></li>',
			'+': '<li><a class="DerivationallyRelatedForm" style="cursor:pointer">' + relationsMenu['derivationallyRelatedForm'] + '</a></li>', '*': '<li><a class="Entailment" style="cursor:pointer">' + relationsMenu['entailment'] + '</a></li>',
			'>': '<li><a class="Cause" style="cursor:pointer">' + relationsMenu['cause'] + '</a></li>', '^': '<li><a class="AlsoSee" style="cursor:pointer">' + relationsMenu['alsoSee'] + '</a></li>',
			'$': '<li><a class="VerbGroup" style="cursor:pointer">' + relationsMenu['verbGroup'] + '</a></li>', '&': '<li><a class="SimilarTo" style="cursor:pointer">' + relationsMenu['similarTo'] + '</a></li>',
			'<': '<li><a class="ParticipleOfVerb" style="cursor:pointer">' + relationsMenu['participleOfVerb'] + '</a></li>', '\\': ['<li><a class="Pertainym" style="cursor:pointer">' + relationsMenu['pertainym'] + '</a></li>',
			'<li><a class="Pertainym" style="cursor:pointer">' + relationsMenu['derivedFromAdjective'] + '</a></li>'],
			';c': '<li><a class="DomainCategory" style="cursor:pointer">' + relationsMenu['domainCategory'] + '</a></li>', '-c': '<li><a class="DomainTermCategory" style="cursor:pointer">' + relationsMenu['domainTermCategory'] + '</a></li>',
			';r': '<li><a class="DomainRegion" style="cursor:pointer">' + relationsMenu['domainRegion'] + '</a></li>', '-r': '<li><a class="DomainTermRegion" style="cursor:pointer">' + relationsMenu['domainTermRegion'] + '</a></li>',
			';u': '<li><a class="DomainUsage" style="cursor:pointer">' + relationsMenu['domainUsage'] + '</a></li>', '-u': '<li><a class="DomainTermUsage" style="cursor:pointer">' + relationsMenu['domainTermUsage'] + '</a></li>',
			'overview': '<li><a class="Overview" style="cursor:pointer">' + relationsMenu['overview'] + '</a></li>', 'concept': '<li><a class="Concept" style="cursor:pointer">' + relationsMenu['concept'] + '</a></li>',
			'sentenceFrame': '<li><a class="SentenceFrame" style="cursor:pointer">' + relationsMenu['sentenceFrame'] + '</a></li>'
		};
		if (!$(event.target.parentNode).parent().parent().hasClass('DerivationallyRelatedForm')) {
			list += '<li><a class="otherLangSearch" style="cursor:pointer">' + relationsMenu['translation'] + '</a></li>';
			if (relations.length === 0) {
				list += '<li>' + relationsMenu['noRelations'] + '</li>';
			}
			else {
				for (var i = 0; i < relations.length; i++) {
					if (relations[i] === '\\') {
						var linesList = relationsMenuLines[relations[i]];
						list += linesList[(pos === 'r' ? 1 : 0)];

					}
					else if (relations[i] === '~') {
						var linesList = relationsMenuLines[relations[i]];
						list += linesList[(pos === 'v' ? 1 : 0)]
					}
					else {
						list += relationsMenuLines[relations[i]];
					}
				}
				list += (pos === 'v' ? relationsMenuLines['sentenceFrame'] : '')
			}
			if ($(event.target.parentNode).find("ul.search").length === 0) {
				$(event.target.parentNode).append('<ul class="expand" id="' + id + '">' + list + '</ul>');
			}
			else {
				$('<ul class="expand" id="'+id+'">' + list + '</ul>').insertBefore($(event.target.parentNode).find("ul.search")[0]);
			}
			$("#"+id+' a').click(function(event){expandedSearch(event)});
		}
		else {
			if (relations.indexOf('+') !== -1) {
				list += relationsMenuLines['+'];
			}
			list += relationsMenuLines['overview'];
			list += relationsMenuLines['concept'];
			if ($(event.target.parentNode).find("ul.search").length === 0) {
				$(event.target.parentNode).append('<ul class="expand" id="' + id + '">' + list + '</ul>');
			}
			else {
				$('<ul class="expand" id="'+id+'">' + list + '</ul>').insertBefore($(event.target.parentNode).find("ul.search")[0]);
			}
			$("#"+id+' a').click(function(event){expandedSearch(event)});
		}
	}
	else {
		if ($(event.target.parentNode).find("ul.search").length === 0) {
			$(event.target.parentNode.children[event.target.parentNode.children.length - 1]).fadeToggle('slow');
		}
		else {
			$(event.target.parentNode).find("ul.expand").fadeToggle('slow');
		}		
	}
}

/**
 * Renders a result not found message
 * @param data is an object from a ajax result call
 */
function notFound(data) {
	$("#results").append(languageSettings('searchNotFound', localStorage.getItem('language')));
}

/**
 * Formats and displays results from a word query
 * @param result is an object
 */
function formattedResults(result) {
	for (var elem in result.relations) {
		if (!info.hasOwnProperty(elem)) {
			info[elem] = {}
		}
		for (var synset in result.relations[elem])
			if (!info[elem].hasOwnProperty(synset)) {
				info[elem][synset] = result.relations[elem][synset];
			}
	}
	searchLangCache = currentSearchLanguage !== undefined ? currentSearchLanguage : null;
	currentSearchLanguage = result.language;
	if (searchLangCache !== null && searchLangCache !== currentSearchLanguage) {
		$(".langmenu").append('<option value="' + CountryToCode(searchLangCache) + '">' + searchLangCache + "</option>");
		if (otherLangs.length !== 0) {
			if (otherLangs.indexOf(CountryToCode(currentSearchLanguage)) !== -1) {
				otherLangs.splice(otherLangs.indexOf(currentSearchLanguage), 1);
				var regex = new RegExp(' ?' + CountryToCode(currentSearchLanguage) + '[,]?');
				var pLangList = $("#pLangList");
				pLangList.text(pLangList.text().replace(regex, ''));
				var text = pLangList.text();
				if (text[text.length - 1] === ',') {
					pLangList.text(text.slice(0,-1))
				}
			}
			if (otherLangs.length === 0) {
				pLangList.html(languageSettings('formLabel', localStorage.getItem('language')) + '<span style="color:#999999">'
					+ languageSettings('noTransLangSelected', localStorage.getItem('language')) + '</span>');
			}
		}
	}
	$('.langmenu option[value="' + CountryToCode(currentSearchLanguage) + '"]').remove();
	$("#results").append('<ul id="resultList"></ul>');
	$("#resultList").append(result.line);
	$("#resultList a").click(function(event){expand(event)});
	$("span.mark").each(function() {
		var lemma = $(this).text();
		$(this).replaceWith('<a style="color:black;font-weight:bold;" href="http://' + location.hostname + ':' + location.port + '/search/s=' + lemma +'&search=normal">' + lemma + '</a>');
	});
	$(".concept").prop('title', languageSettings('concept', localStorage.getItem('language')));
	$('[data-tool-tip=tooltip]').tooltip({trigger:'hover', container:'body'});
	var lis = document.getElementsByTagName('li');
	var id;
	for (var i = 0; i < lis.length; i++) {
		if (lis[i].className.search('select2') === -1) {
			id = i;
			break;
		}
	}
	advancedSearchLangs(lis[id].className, true);
	var posTranslations = partOfSpeechList(localStorage.getItem('language'));
	$("h2.pos").each(function() {
		$(this).text(posTranslations[$(this).text()]);
	});
}

/**
 * Upon a collision of languages in the search for a result, it displays a popup to the user to select a language
 * @param languages is an array of strings
 */
function languageCollisionMenu(languages) {
	$('body').append('<div class="pop-up"><div class="content"><div class="popup-container"><i class="material-icons close" id="popup-close">cancel</i><p class="collision-p">' +
		languageSettings('collision', localStorage.getItem('language')) +
		'</p><br><select id="collisionSelect"></select></div></div></div>');
	$("#collisionSelect").append('<option value="" disabled selected>Choose a language</option>');
	for (var i = 0; i < languages.length; i++) {
		$("#collisionSelect").append('<option value=' + languages[i] + '>' + languages[i] + '</option>');
	}
	$("#collisionSelect").select2();
	$("#collisionSelect").on('select2:select', function(e) {
		$.ajax({type:'GET',url:'.', data:'s=' + String(currentSearchTerm) + '&st=norm1' + '&language=' + e.params.data.id}).done(function(data){if(data.found === 1){formattedResults(data)} else{notFound(data)}});
		$("#popup-close").click();
	});
	$("#popup-close").click(function(){
		$("#popup-close").unbind('click');
		$(".pop-up").remove();
	});
}

/**
 * Renders result boxes and requests a word search
 * @param searchTerm is a String
 */
function search(searchTerm) {
	var found;
	currentSearchTerm = searchTerm;
    if ($("#searchResultBox")) {
        $("#searchResultBox").remove()
    }
	$("body").append('<div class="container" id="searchResultBox" style="margin-top:5%;max-height:90vh;"><div class="row vertical-center-row"><div class="col-md-9" id="results" style="overflow:hidden"></div><div class="col-md-3" id="langResults" style="padding:0 !important;max-height:90vh;overflow-y:scroll;-ms-overflow-y:scroll;"></div></div>');
    history.pushState(null, null, '/search/s=' + String(searchTerm));
    var result = $.ajax({type:'GET',url:'.', data:'s=' + String(searchTerm) + '&st=norm1' + '&language=UNK'}).done(function(data){if (data.collision === 1) {languageCollisionMenu(data.languages)} else if(data.found === 1){formattedResults(data);found=true;} else{notFound(data);found=false;}});
}

/**
 * Renders the results of a translation request for a first time
 * @param data is an Object
 */
function advancedSearchLangsAppender(data) {
	var language = localStorage.getItem('language');
	var countryCodeList = CodeToCountry(language);
	var wikipediaList = wikipediaLinkList(language);
	var deflabel = languageSettings('defLabel', language);
	var concept = languageSettings('transConcept', language);
	if ($("#langResults div").length === 0) {
		$("#langResults").css({'border':'1px solid black'});
	}
	else {
		$("#langResults").empty();
	}
	if (data.hasOwnProperty("mismatch")) {
		$("#langResults").append('<div><p><span style="color:red">' + languageSettings('mismatchText', language) + '</span></p></div>');
	}
	else {
		for (var elem in data) {
			var languageName = countryCodeList[elem];
			var link = wikipediaList[elem];
			var lemma = '';
			if (data[elem]['lemma'].length) {
				lemma = data[elem]['lemma']
			}
			if (elem === otherLangs[otherLangs.length - 1]) {
				$("#langResults").append('<div id="' + elem + 'Results" style="padding-left:15px;padding-right:15px;"><h4><a href="' + link + '" target="_blank">' + languageName + '</a></h4></div>');
				$("#" + elem + 'Results').append('<p><span style="color:red">' + concept + ': </span>' + lemma + '</p>');
				if (data[elem]['def'].length) {
					$("#" + elem + 'Results').append('<p><span style="color:red">' + deflabel + '</span>: ' + data[elem]['def'][0] + '</p>');
				}
			}
			else {
				$("#langResults").append('<div id="' + elem + 'Results" style="padding-left:15px;padding-right:15px;"><h4><a href="' + link + '" target="_blank">' + languageName + '</a></h4></div>');
				$("#" + elem + 'Results').append('<p><span style="color:red">' + concept + ': </span>' + lemma + '</p>');
				if (data[elem]['def'].length) {
					$("#" + elem + 'Results').append('<p><span style="color:red">' + deflabel + '</span>: ' + data[elem]['def'][0] + '</p>');
				}
				$("#langResults").append('<div style="width:100%;margin:0;border-bottom:1px solid black"></div>');
			}
		}
	}
}

/**
 * Renders results from a translation request for a single language(added on top of the already displayed)
 * @param data is an Object
 */
function advancedSearchSingleLang(data) {
	var language = localStorage.getItem('language');
	var countryCodeList = CodeToCountry(language);
	var wikipediaList = wikipediaLinkList(language);
	var deflabel = languageSettings('defLabel', language);
	var concept = languageSettings('transConcept', language);
	if ($("#langResults div").length === 0) {
		$("#langResults").css({'border':'1px solid black'});
	}
	if (data.hasOwnProperty("mismatch")) {
		if ($("#langResults div").length === 0) {
			$("#langResults").append('<div><p><span style="color:red">Interlingual paring mismatch</span></p></div>');
		}
	}
	else {
		for (var elem in data) {
			var lemma = '';
			if (data[elem]['lemma'].length) {
				lemma = data[elem]['lemma']
			}
			var languageName = countryCodeList[elem];
			var link = wikipediaList[elem];
			if ($("#langResults div").length > 0) {
				$("#langResults").append('<div style="width:100%;margin:0;border-bottom:1px solid black"></div>');
			}
			$("#langResults").append('<div id="' + elem + 'Results" style="padding-left:15px;padding-right:15px;"><h4><a href="' + link + '" target="_blank">' + languageName + '</a></h4></div>');
			$("#" + elem + 'Results').append('<p><span style="color:red">' + concept + ': </span>' + lemma + '</p>');
			if (data[elem]['def'].length) {
				$("#" + elem + 'Results').append('<p><span style="color:red">' + deflabel + '</span>: ' + data[elem]['def'][0] + '</p>');
			}
		}
	}
}

/**
 * Upon a translation request by the user, the server will be queried for results
 * @param event is an Object
 * @param classKnown is a boolean
 */
function advancedSearchLangs(event, classKnown=false) {
	var offset;
	var pos;
	if (!classKnown) {
		var className = $(event.target.parentNode).parent().parent().prop('class');
		offset = className.slice(0, className.length - 2);
		currentTranslatedOffset = className;
		pos = className[className.length - 1];
	}
	else {
		currentTranslatedOffset = event;
		offset = event.slice(0, event.length - 2);
		pos = event[event.length - 1];
	}
	if ($(".langmenu").select2('data').length !== 0) {
        $.ajax({type:'GET',url:'.', data:'o=' + String(offset) + '&langs=' + JSON.stringify(otherLangs) + '&c=' + pos + '&st=advsearch' + '&language=' + currentSearchLanguage}).done(function(data){advancedSearchLangsAppender(data.result)});
    }
}

function main() {
	if (localStorage.getItem('language') === null) {
		localStorage.setItem('language', 'English');
	}
	var language = localStorage.getItem('language');
	switch (language) {
		case 'Portuguese':
			$('.Portuguese').css('font-weight', 'bold');
			break;
		case 'English':
			$(".English").css('font-weight', 'bold');
			break;
		case 'French':
			$(".French").css('font-weight', 'bold');
			break;
		case 'Chinese':
			$(".Chinese").css('font-weight', 'bold');
			break;
	}
	$(".language").click(function() {
		var language = $(this).prop("class").split(' ')[1];
		if (implementedLanguageList().indexOf(language) !== -1) {
			localStorage.setItem('language', language);
			location.reload();
		}
		else {
			$('body').append('<div class="pop-up"><div class="content"><div class="popup-container"><a href="http://lx-wordnetbrowser.readthedocs.io/en/latest/translations.html"' +
				'target="_blank" class="topRight"><img class="popup-img" src="/static/assets/images/GitHub-Mark-120px-plus.png">' +
				'</a><i class="material-icons close" id="popup-close">' +
				'cancel</i><p class="pop-up-p">' + $(this).text() + ' is not ' +
				'implemented yet. If you are fluent and would like to help, click on the image above to find out more.' +
				'</p></div></div></div>');
			$("#popup-close").click(function(){
				$("#popup-close").unbind('click');
				$(".pop-up").remove();
			});
		}
	});
	$("#formLabel").text(languageSettings('formLabel', language));
	$("#searchInput").prop('placeholder', languageSettings('search', language));
	$("#normal-search").prop('title', languageSettings('search', language));
	$("#globe").prop('title', languageSettings('globe', language));
	$("#advanced-search").prop('title', languageSettings('search', language));
	$("#langSelectBox").prop('title', languageSettings('languageChange', language));
	var countryCodeList = CodeToCountry(language);
	for (var elem in countryCodeList) {
		if (countryCodeList[elem] !== currentSearchLanguage) {
			$(".langmenu").append('<option value="' + elem + '">' + countryCodeList[elem] + '</option>');
		}
	}
	$('[data-tool-tip=tooltip]').tooltip({trigger:'hover'});
    $("#normal-search").click(function() {
    	if ($("#searchInput").val() !== '') {
    		search($("#searchInput").val(),false);
    	}
    	otherLangs = $(".langmenu").val();
    	if ($("#pLangList").length > 0) {
			$("#pLangList").remove();
			$(window).unbind('resize');
		}
		$("#langListTarget").append('<p id="pLangList"></p>');
		$("#pLangList").offset({left:String($("#searchInput").offset().left)});
		$(window).resize(function() {
			$("#pLangList").offset({left:String($("#searchInput").offset().left)});
		});
		var startPhrase = languageSettings('formLabel', language);
		var noLangsFound = languageSettings('noTransLangSelected', language);
		if (otherLangs.length > 0 ) {
            for (var i = 0;i < otherLangs.length; i++) {
                if (i === 0) {
                    $("#pLangList").text(startPhrase + otherLangs[i]);
                }
                else {
                    $("#pLangList").text($("#pLangList").text() + ', ' + otherLangs[i]);
                }
            }
        }
        else {
			$("#pLangList").html(startPhrase + '<span style="color:#999999">' + noLangsFound + '</span>');
		}
    });
    $("#searchInput").keypress(function(e) {
    	var key = e.which;
    	if (key == 13) {
    		$("#normal-search").click();
    	}
    });
    if(location.pathname !== '/') {
    	var queryWord = location.pathname.split('&')[0].slice(10);
    	$("#searchInput").val(decodeURI(queryWord));
    	$("#normal-search").click();
    }
    $(".langmenu").select2();
    $(".langmenu").on('select2:unselect',function(event) {
    	if (!event.params.originalEvent) {
    		return
    	}
    	event.params.originalEvent.stopPropagation();
    });
    $(".langmenu").on('select2:unselect', function(e) {
    	otherLangs.splice(otherLangs.indexOf(e.params.data.id), 1);
		var regex = new RegExp(' ?' + e.params.data.id + '[,]?');
		$("#pLangList").text($("#pLangList").text().replace(regex, ''));
		var text = $("#pLangList").text();
		if (text[text.length - 1] === ',') {
			$("#pLangList").text(text.slice(0,-1))
		}
		if (otherLangs.length === 0) {
			$("#pLangList").html($("#pLangList").text() + ' ' + '<span style="color:#999999">' + languageSettings('noTransLangSelected', localStorage.getItem('language')) + '</span>');
		}
		if ($("#langResults").length !== 0) {
			var langObj = $("#" + e.params.data.id + 'Results');
			if (langObj.is(':first-child')) {
				langObj.next().remove();
				langObj.remove();
			}
			else {
				langObj.prev().remove();
				langObj.remove();
			}
		}
		if (otherLangs.length === 0) {
			$("#langResults").css({'border':'none'})
		}
	});
    $(".langmenu").on('select2:select', function(e) {
		if (otherLangs.length === 0) {
			$("#pLangList").text(languageSettings('formLabel', localStorage.getItem('language')) + e.params.data.id);
		}
		else {
			$("#pLangList").text($("#pLangList").text() + ', ' + e.params.data.id);
		}
    	otherLangs.push(e.params.data.id);
    	if (currentTranslatedOffset !== undefined) {
    		var offset = currentTranslatedOffset.slice(0, currentTranslatedOffset.length - 2);
    		var pos = currentTranslatedOffset[currentTranslatedOffset.length - 1];
			$.ajax({type:'GET',url:'.', data:'o=' + String(offset) + '&langs=' + JSON.stringify([e.params.data.id]) + '&c=' + pos + '&st=advsearch' + '&language=' + currentSearchLanguage}).done(function(data){advancedSearchSingleLang(data.result)});
		}
	});
    $("#parent-dropdown").on('hide.bs.dropdown',function(){
    	$(".langmenu").select2('close');
    });
    $("#langSelectList").on('select2:select', function(){
    	if (implementedLanguageList().indexOf($("#langSelectList").val()) !== -1) {
    		localStorage.setItem('language', $("#langSelectList").val());
    		location.reload();
		}
		else {
			$('body').append('<div class="pop-up"><div class="content"><div class="popup-container"><a href="http://lx-wordnetbrowser.readthedocs.io/en/latest/translations.html"' +
				'target="_blank" class="topRight"><img class="popup-img" src="/static/assets/images/GitHub-Mark-120px-plus.png">' +
				'</a><i class="material-icons close" id="popup-close">' +
				'cancel</i><p class="pop-up-p">' + $("#langSelectList").val() + ' is not ' +
				'implemented yet. If you are fluent and would like to help, click on the image above to find out more.' +
				'</p></div></div></div>');
			$("#popup-close").click(function(){
				$("#popup-close").unbind('click');
				$(".pop-up").remove();
			});
		}
	});
    $(".invis").width($("#langSelectList").width()).height($("#langSelectList").height()).css({'border-radius':$("#langSelectList").css('border-radius'),'-webkit-border-radius': $("#langSelectList").css('-webkit-border-radius'), '-moz-border-radius': $("#langSelectList").css('-moz-border-radius')});
	var languages = languageList();
	$("#langSelectList").append('<option value="" disabled selected>' + languageSettings('langSelect', language) + '</option>');
	for (var i = 0; i < languages.length; i++) {
		$("#langSelectList").append('<option value="' + languages[i] + '">' + languages[i] + '</option>');
	}
	$("#langSelectList").select2();
	$("#references").prop("href", 'http://' + location.hostname + ':' + location.port + '/references.html');
	$("#header").append('<span style="font-family: Bebas Neue, sans-serif; font-size:15px;" id="Node">' + nodeText + '</span>');
	$("#Node").offset({left: $("img.headerImage").offset().left + 43, top: $("img.headerImage").offset().top + 125});

}
$(document).ready(function(){main()});