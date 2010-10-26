$('a#update').click(function() {
	$.getJSON('/streik.json', function(data) {
		var answer = data['streik'] ? 'Ja' : 'Nein';
		$('#answer').removeClass().addClass(answer).text(answer);
		document.title = data['title'];
		$('.twitter-share-button').data['text'] = data['twitter_text'];
	});
	return false;
});