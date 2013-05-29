function list(winTabs) {
		
	if(winTabs != null)
	{		
		totalTabs = winTabs.length;
		for (var j=0; j<totalTabs;j++) 
		{          
			currentTabId = winTabs[j].id;
			chrome.tabs.get (currentTabId, getTab);				
		}
	}		
}

function getTab(t)
{	
	var url = t.url;
	var title = t.title;
	
	PopulateCheckboxList(t.id, url, title);
}

function PopulateCheckboxList(id, url, title)
{	
		$('#url_list_cbs').append($('<li/>')
					    .append($('<input/>', 
								{
									'type': 'checkbox',
									'id'  :	'cb' + id,			
									'name':	'cb' + id													
								}))
								.click (function (event)
								{
									if($('#cb'+id).is(':checked')) {
										finalURLsList[id] = title + " -- "+ url + '\n\n';
									}							
									else
									{
										delete finalURLsList[id];
									}									
								})
								.append($('<label/>', 
								{													
									'text': title
								})));

}



function PickURLS()
{
	gContents = '';	 	
	finalURLsList = {};
	$('#url_list_cbs').empty();
	
	$('#alertmsg').text("Please select some URLs");
	$("#alert").removeClass("alert-success").removeClass("alert-error").addClass("alert-info");
	
	$("#alert").css('visibility','visible');		
	$("#url-list_ta").css('visibility','hidden');
	$("#url_list_cbs").css('visibility','visible');	
	
	$("#eventSelected").text("GMail");
	
	chrome.tabs.query({'windowId': chrome.windows.WINDOW_ID_CURRENT},list);    	
}

function BeamURLS()
{		
	$('#alertmsg').text("Please paste the URLs you want to Beam!!");
	$("#alert").removeClass("alert-success").removeClass("alert-error").addClass("alert-info");
	
	$("#alert").css('visibility','visible');	
	$("#url-list_ta").css('visibility','visible');
	$("#url_list_cbs").css('visibility','hidden');	
	
	$("#eventSelected").text("Beam");
}

$(document).ready(function() {	
	
	$("#tabs").tabs();	
	PickURLS();

	$("#tabs ul li a").click(function () {
        var divSelected = this.href;
		var toMatch = "PickedUrlsContainer";		
		var index = divSelected.indexOf(toMatch);
			
		if(index >= 0)
		{
			Operation =0;
			PickURLS();	
		}
		else
		{
			Operation =1;
			BeamURLS();
		}		
    });	
});

$("#eventSelected").click(function(){
	if(Operation === 0)
	{
		SendGMail();	
	}
	else if(Operation === 1)
	{
		OpenBeamedURLs();	
	}
});


function SendGMail()
{
	if(0 === Object.size(finalURLsList))
	{
		$("#alert").removeClass("alert-info").addClass("alert-error");
		$("#alertmsg").text("Please select some URLs");
		return;
	}
	else
	{
		$("#alert").removeClass("alert-info").removeClass("alert-error").addClass("alert-success");
		$("#alertmsg").text("Selected URLs are ready to be sent through GMail");	
	}
	
	$.each( finalURLsList, function( key, value ) {
		gContents = gContents + value;		
	});
	
	var msg = CleanMessage(gContents);
	
	sendGmail({
		to: 'clicksuku@gmail.com',
		subject: 'List of URLs',
		message: msg
	});	
}

function StripTheURL(url)
{
	var indStart = url.indexOf("--") + 3;
	var indEnd = url.length - indStart;
	var desiredURL =  url.substr(indStart, indEnd);	
	return desiredURL;
}

function BeamItOnChrome(URLList)
{
	for(var i=0;i< URLList.length; i++)
	{	
		//alert(URLList[i]);
		//chrome.windows.create({url: URLList[i], type: "normal"});
		window.open(URLList[i], '_blank');
	}
}

function OpenBeamedURLs()
{
	var textAreaText = $("#url-list_ta").val();
	if(textAreaText.length === 0)
	{
		$("#alert").removeClass("alert-info").addClass("alert-error");
		$("#alertmsg").text("Please fill some URLs to beam");
		return;
	}
	else
	{
		$("#alert").removeClass("alert-info").removeClass("alert-error").addClass("alert-success");
		$("#alertmsg").text("Selected URLs are ready to be beamed to Chrome");	
	}
	
	var beamURLsList = textAreaText.split("\n\n");	
	var URLList = beamURLsList.map(StripTheURL);
	
	BeamItOnChrome(URLList);	
}

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function CleanMessage(message)
{	
	var encodedMsg = encodeURIComponent(message);	
	return encodedMsg;
}

var sendGmail = function(opts){
    	
	var str = 'https://mail.google.com/mail/?view=cm&fs=1'+
              '&to=' + opts.to +
              '&su=' + opts.subject +
              '&body=' + opts.message +
              '&ui=1';
    
	window.open(str,'_newtab');	
}


var Operation = 0;
var gContents = '';	
var totalTabs = -1;
var currentTabId = -1;
var finalURLsList = {};

 
 