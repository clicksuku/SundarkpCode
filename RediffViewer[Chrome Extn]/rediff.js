$('a'[href$='htm'],[href$='html']).each(function(){
	this.href += '?print=true';
});