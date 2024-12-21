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
										finalURLsList.push(id);
									}							
									else
									{
										finalURLsList.splice($.inArray(id, finalURLsList),1);										
									}									
								})
								.append($('<label/>', 
								{													
									'text': title
								})));

}



function PickURLS()
{	
	finalURLsList = new Array();
	$('#url_list_cbs').empty();		
	chrome.tabs.query({},list);    	
}

$(document).ready(function() {		
	$("#tabs").tabs();		
	PickURLS();		
});

$("#eventSelected").click(function(){
	if(1 >= finalURLsList.length)
	{
		$("#alert").removeClass("alert-info").addClass("alert-error");
		$("#alertmsg").text("Please select atleast two tabs to switch");
		return;
	}
	else
	{
		$("#alert").removeClass("alert-info").removeClass("alert-error").addClass("alert-success");
		$("#alertmsg").text("Selected tabs are ready for switching");	
	}
	
	chrome.runtime.sendMessage({data : finalURLsList},
        function (response) {
            console.log("Success");
        });	
	window.close();	
});


var totalTabs = -1;
var currentTabId = -1;
var finalURLsList = new Array();
 