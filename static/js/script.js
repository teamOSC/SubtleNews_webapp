$('#menu_btn').sidr();

$('#play').click(function(){
	//alert('foo');
	var text = 'food chamber';
	var audio = document.createElement('audio');
	audio.setAttribute('src', 'http://developer.mozilla.org/@api/deki/files/2926/=AudioTest_(1).ogg');
	audio.load();
	audio.play();
	return false;
});

