"use strict";
var currentSearchTerm;
var info = {};
var otherLangs = [];
var currentTranslatedOffset;
var relationsShort = {'DirectHypernym': 'dhype', 'DirectHyponym': 'dhypo', 'InheritedHypernym':'ihype', 'FullHyponym': 'fhypo', 'MemberHolonym': 'mh', 'SubstanceHolonym': 'sh', 'PartHolonym': 'ph', 'MemberMeronym': 'mm', 'SubstanceMeronym': 'sm', 'PartMeronym': 'pm', 'Antonym': 'ant', 'InstanceHypernym': 'inhype', 'InstanceHyponym': 'inhypo', 'Attribute': 'attr', 'DerivationallyRelatedForm': 'derform', 'Entailment': 'ent', 'Cause': 'ca', 'AlsoSee': 'asee', 'VerbGroup': 'vgr', 'SimilarTo': 'sto', 'ParticipleOfVerb': 'pverb', 'Pertainym': 'per'};
var partOfSpeech = {'n': 'noun', 'v': 'verb', 'a': 'adj', 's': 'adj', 'r': 'adv'};
var main_language = 'English';

function expandedSearchFormatter(data,event,remove) {
	for (var elem in data.relations) {
		for (var element in data.relations[elem]) {
			if (!info[elem].hasOwnProperty(element)) {
				info[elem][element] = data.relations[elem][element];
			}
		}
	}
	if (remove) {
		$(event.target.parentNode.children[2]).remove();
	}
	$(event.target.parentNode).append('<ul>' + data.line + '</ul>');
	if (event.target.className === 'DirectHypernym' || event.target.className === 'DirectHyponym' || event.target.className === 'InheritedHypernym' || event.target.className === 'FullHyponym') {
		$(event.target.parentNode.children[2]).find('a').click(function(event){expand(event)});
		$("span.mark").each(function() {
			var lemma = $(this).text();
			$(this).replaceWith('<a style="color:black;font-weight:bold;" href="http://' + String(location.hostname) + ':8000/search/s=' + lemma +'&search=normal">' + lemma + '</a>');
		});
		$(event.target.parentNode.children[2]).addClass(event.target.className+' search');
		$(event.target.parentNode.children[2]).find("ul").addClass('search');
	}
	else {
		$(event.target.parentNode.children[1]).find('a').click(function(event){expand(event)});
		$("span.mark").each(function() {
			var lemma = $(this).text();
			$(this).replaceWith('<a style="color:black;font-weight:bold;" href="http://' + String(location.hostname) + ':8000/search/s=' + lemma +'&search=normal">' + lemma + '</a>');
		});
		$(event.target.parentNode.children[1]).addClass(event.target.className + ' search');
		$(event.target.parentNode.children[1]).find("ul").addClass('search');
	}
	var language = localStorage.getItem('language');
	$(".concept").prop('title', languageSettings('concept', language));
	$('[data-tool-tip=tooltip]').tooltip({trigger:'hover', container:'body'});
}

function expandRequest(event, remove=false) {
	var searchTypeParsed = relationsShort[event.target.className];
	var className = $(event.target.parentNode).parent().parent().prop('class');
	var offset = className.slice(0, className.length - 2);
	var pos = className[className.length - 1];
	history.pushState(null,null,'/search/s=' + currentSearchTerm + '&o=' + offset + '&t=' + searchTypeParsed + '&c=' + pos);
	$.ajax({type:'GET',url:'.', data:'s='+ currentSearchTerm + '&o=' + offset + '&t=' + searchTypeParsed + '&c=' + pos}).done(function(data){expandedSearchFormatter(data, event, remove)});
}

function expandedSearch(event) {
	if (event.target.className !== 'otherLangSearch') {
		if ($(event.target.parentNode).find("ul.search").length !== 0) {
			if (event.target.className === 'DirectHypernym' || event.target.className === 'InheritedHypernym' || event.target.className === 'DirectHyponym' || event.target.className === 'FullHyponym') {
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

function expand(event) {
	if ($(event.target.parentNode).find("ul.expand").length === 0) {
		var list = '';
		var pos = event.target.parentNode.className[event.target.parentNode.className.length - 1];
		var offset = event.target.parentNode.className.slice(0, event.target.parentNode.className.length - 2);
		var relations = info[partOfSpeech[pos]][offset];
		var id = String($("ul.expand").length);
		var relationsMenu = languageSettings('relationsMenu', localStorage.getItem('language'));
		var relationsMenuLines = {'@': '<li><a class="DirectHypernym" style="cursor:pointer">' + relationsMenu['directHypernym'] + '</a> | <a class="InheritedHypernym" style="cursor:pointer">' + relationsMenu['inheritedHypernym'] + '</a></li>',
			'~': '<li><a class="DirectHyponym" style="cursor:pointer">' + relationsMenu['directHyponym'] + '</a> | <a class="FullHyponym" style="cursor:pointer">' + relationsMenu['fullHyponym'] + '</a></li>',
			'#m': '<li><a class="MemberHolonym" style="cursor:pointer">' + relationsMenu['memberHolonym'] + '</a></li>', '#s': '<li><a class="SubstanceHolonym" style="cursor:pointer">' + relationsMenu['substanceHolonym'] + '</a></li>',
			'#p': '<li><a class="PartHolonym" style="cursor:pointer">' + relationsMenu['partHolonym'] + '</a></li>', '%m': '<li><a class="MemberMeronym" style="cursor:pointer">' + relationsMenu['memberMeronym'] + '</a></li>',
			'%s': '<li><a class="SubstanceMeronym" style="cursor:pointer">' + relationsMenu['substanceMeronym'] + '</a></li>', '%p': '<li><a class="PartMeronym" style="cursor:pointer">' + relationsMenu['partMeronym'] + '</a></li>',
			'!': '<li><a class="Antonym" style="cursor:pointer">' + relationsMenu['antonym'] + '</a></li>', '@i': '<li><a class="InstanceHypernym" style="cursor:pointer">' + relationsMenu['instanceHypernym'] + '</a></li>',
			'~i': '<li><a class="InstanceHyponym" style="cursor:pointer">' + relationsMenu['instanceHyponym'] + '</a></li>', '=': '<li><a class="Attribute" style="cursor:pointer">' + relationsMenu['attribute'] + '</a></li>',
			'+': '<li><a class="DerivationallyRelatedForm" style="cursor:pointer">' + relationsMenu['derivationallyRelatedForm'] + '</a></li>', '*': '<li><a class="Entailment" style="cursor:pointer">' + relationsMenu['entailment'] + '</a></li>',
			'>': '<li><a class="Cause" style="cursor:pointer">' + relationsMenu['cause'] + '</a></li>', '^': '<li><a class="AlsoSee" style="cursor:pointer">' + relationsMenu['alsoSee'] + '</a></li>',
			'$': '<li><a class="VerbGroup" style="cursor:pointer">' + relationsMenu['verbGroup'] + '</a></li>', '&': '<li><a class="SimilarTo" style="cursor:pointer">' + relationsMenu['similarTo'] + '</a></li>',
			'<': '<li><a class="ParticipleOfVerb" style="cursor:pointer">' + relationsMenu['participleOfVerb'] + '</a></li>', '\\': '<li><a class="Pertainym" style="cursor:pointer">' + relationsMenu['pertainym'] + '</a></li>'};
		list += '<li><a class="otherLangSearch" style="cursor:pointer">' + relationsMenu['translation'] + '</a></li>';
		if (relations.length === 0) {
			list += '<li>' + relationsMenu['noRelations'] + '</li>';
		}
		else {
			for (var i = 0; i < relations.length; i++) {
				if (relations[i] !== '+') {
					list += relationsMenuLines[relations[i]];	
				}
			}
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
		if ($(event.target.parentNode).find("ul.search").length === 0) {
			$(event.target.parentNode.children[event.target.parentNode.children.length - 1]).fadeToggle('slow');
		}
		else {
			$(event.target.parentNode).find("ul.expand").fadeToggle('slow');
		}		
	}
}

function notFound(data) {
	$("#results").append(languageSettings('searchNotFound', localStorage.getItem('language')));
}

function formattedResults(result) {
	for (var elem in result.relations) {
		if (!info.hasOwnProperty(elem)) {
			info[elem] = result.relations[elem];
		}
	}
	$("#results").append('<ul id="resultList"></ul>');
	$("#resultList").append(result.line);
	$("#resultList a").click(function(event){expand(event)});
	$("span.mark").each(function() {
		var lemma = $(this).text();
		$(this).replaceWith('<a style="color:black;font-weight:bold;" href="http://' + String(location.hostname) + ':8000/search/s=' + lemma +'&search=normal">' + lemma + '</a>');
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
}

function search(searchTerm) {
	var found;
	currentSearchTerm = searchTerm;
    if ($("#searchResultBox")) {
        $("#searchResultBox").remove()
    }
	$("body").append('<div class="container" id="searchResultBox" style="margin-top:5%;max-height:90vh;"><div class="row vertical-center-row"><div class="col-md-9" id="results" style="overflow-x:scroll"></div><div class="col-md-3" id="langResults" style="padding:0 !important;max-height:90vh;overflow-y:scroll;"></div></div>');
    history.pushState(null, null, '/search/s=' + String(searchTerm));
    var result = $.ajax({type:'GET',url:'.', data:'s=' + String(searchTerm)}).done(function(data){if(data.found === 1){formattedResults(data);found=true;} else{notFound(data);found=false;}});
}

function advancedSearchLangsAppender(data) {
	var language = localStorage.getItem('language');
	var countryCodeList = countryCodes(language);
	var wikipediaList = wikipediaLinkList(language);
	var deflabel = languageSettings('defLabel', language);
	if ($("#langResults div").length === 0) {
		$("#langResults").css({'border':'1px solid black'});
	}
	else {
		$("#langResults").empty();
	}
	for (var elem in data) {
        var languageName = countryCodeList[elem];
        var concept = languageSettings('transConcept', language);
        var link = wikipediaList[elem];
        if (elem === otherLangs[otherLangs.length - 1]) {
            $("#langResults").append('<div id="' + elem + 'Results" style="padding-left:15px;padding-right:15px;"><h4><a href="' + link + '" target="_blank">' + languageName + '</a></h4></div>');
            $("#" + elem + 'Results').append('<p><span style="color:red">' + concept + ': </span>' + data[elem]['lemma'] + '</p>');
            if (elem === 'en') {
                $("#" + elem + 'Results').append('<p><span style="color:red">' + deflabel + '</span>: ' + data[elem]['def'] + '</p>');
            }
        }
        else {
            $("#langResults").append('<div id="' + elem + 'Results" style="padding-left:15px;padding-right:15px;"><h4><a href="' + link + '" target="_blank">' + languageName + '</a></h4></div>');
            $("#" + elem + 'Results').append('<p><span style="color:red">' + concept + ': </span>' + data[elem]['lemma'] + '</p>');
            if (elem === 'en') {
                $("#" + elem + 'Results').append('<p><span style="color:red">' + deflabel + '</span>: ' + data[elem]['def'] + '</p>');
            }
            $("#langResults").append('<div style="width:100%;margin:0;border-bottom:1px solid black"></div>');
        }
    }
}

function advancedSearchSingleLang(data) {
	var language = localStorage.getItem('language');
	var countryCodeList = countryCodes(language);
	var wikipediaList = wikipediaLinkList(language);
	var deflabel = languageSettings('defLabel', language);
	if ($("#langResults div").length === 0) {
		$("#langResults").css({'border':'1px solid black'});
	}
	for (var elem in data) {
		var languageName = countryCodeList[elem];
		var concept = languageSettings('transConcept', language);
		var link = wikipediaList[elem];
		if ($("#langResults div").length > 0) {
            $("#langResults").append('<div style="width:100%;margin:0;border-bottom:1px solid black"></div>');
        }
		$("#langResults").append('<div id="' + elem + 'Results" style="padding-left:15px;padding-right:15px;"><h4><a href="' + link + '" target="_blank">' + languageName + '</a></h4></div>');
		$("#" + elem + 'Results').append('<p><span style="color:red">' + concept + ': </span>' + data[elem]['lemma'] + '</p>');
		if (elem === 'en') {
			$("#" + elem + 'Results').append('<p><span style="color:red">' + deflabel + '</span>: ' + data[elem]['def'] + '</p>');
		}
	}
}

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
        $.ajax({type:'GET',url:'.', data:'o=' + String(offset) + '&langs=' + JSON.stringify(otherLangs) + '&c=' + pos}).done(function(data){advancedSearchLangsAppender(data.result)});
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
			$('body').append('<div class="pop-up"><div class="content"><div class="popup-container"><a href="https://' +
				'github.com/nlx-group/Pluricentric-Global-Wordnet/wiki/Translations,-a-community-helping-hand" ' +
				'target="_blank" class="topRight"><img class="popup-img" src="/static/assets/images/GitHub-Mark-120px-plus.png">' +
				'</a><i class="material-icons close" id="popup-close">' +
				'cancel</i><p>' + $("#langSelectList").val() + ' is not ' +
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
	var countryCodeList = countryCodes(language);
	for (var elem in countryCodeList) {
		if (countryCodeList[elem] !== main_language) {
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
		var startPhrase = languageSettings('startPhrase', language);
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
			$("#pLangList").text(startPhrase + noLangsFound);
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
			$("#pLangList").text($("#pLangList").text() + ' ' + languageSettings('noTransLangSelected', localStorage.getItem('language')));
		}
		if ($("#langResults").length !== 0) {
			var langObj = $("#" + e.params.data.id + 'Results');
			langObj.prev().remove();
			langObj.remove();
		}
		if (otherLangs.length === 0) {
			$("#langResults").css({'border':'none'})
		}
	});
    $(".langmenu").on('select2:select', function(e) {
		if (otherLangs.length === 0) {
			$("#pLangList").text(languageSettings('startPhrase', localStorage.getItem('language')) + e.params.data.id);
		}
		else {
			$("#pLangList").text($("#pLangList").text() + ', ' + e.params.data.id);
		}
    	otherLangs.push(e.params.data.id);
    	if (currentTranslatedOffset !== undefined) {
    		var offset = currentTranslatedOffset.slice(0, currentTranslatedOffset.length - 2);
    		var pos = currentTranslatedOffset[currentTranslatedOffset.length - 1];
			$.ajax({type:'GET',url:'.', data:'o=' + String(offset) + '&langs=' + JSON.stringify([e.params.data.id]) + '&c=' + pos}).done(function(data){advancedSearchSingleLang(data.result)});
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
			$('body').append('<div class="pop-up"><div class="content"><div class="popup-container"><a href="https://' +
				'github.com/nlx-group/Pluricentric-Global-Wordnet/wiki/Translations,-a-community-helping-hand" ' +
				'target="_blank" class="topRight"><img class="popup-img" src="/static/assets/images/GitHub-Mark-120px-plus.png">' +
				'</a><i class="material-icons close" id="popup-close">' +
				'cancel</i><p>' + $("#langSelectList").val() + ' is not ' +
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
	for (var i = 0; i < languages.length; i++) {
		$("#langSelectList").append('<option value="' + languages[i] + '">' + languages[i] + '</option>');
	}
	$("#langSelectList").select2();

}
$(document).ready(function(){main()});