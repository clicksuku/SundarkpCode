console.log("Iam inside content script")

$('a').each(function(){
	var url = this.href;
	var htm = "htm";
	if(url.indexOf(htm) > -1)
		this.href += '?print=true';
});