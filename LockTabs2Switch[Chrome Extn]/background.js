chrome.commands.onCommand.addListener(function(command) {
	if(command == "switch")
	{
		chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs) {
				currentTabID = tabs[0].id;			
				SwitchTabs();
		});	
	}  
});

function SwitchTabs()
{
	var loc = finalURLsList.indexOf(currentTabID);
	
	if(loc != -1)		
	{		
		var nextTab = loc + 1;
		if(nextTab >= finalURLsList.length)
		{
			nextTab = 0;
		}						
	}
	else
	{
		nextTab = 0;
	}
	
	if(finalURLsList.length > 0)
	{
		nextTabId = finalURLsList[nextTab];
		chrome.tabs.update(nextTabId, {"active":true,"highlighted":true}, function(tab){
			var window = tab.windowId;
			if(window)
			{
				chrome.windows.update(window, {"focused":true});
			}
		});
	}
}


chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) {
	var loc = finalURLsList.indexOf(tabId);
	
	if(loc != -1)			
	{
		finalURLsList.splice($.inArray(tabId, finalURLsList),1);		
		SwitchTabs();
	}
	
	if(finalURLsList.length <= 0)
	{
		finalURLsList = new Array();
		currentBrowserActionState = "Open";
		SetOpenBrowserActionState();	
	}
	
});


chrome.tabs.onActivated.addListener(function(activeInfo) {
	var tabId = activeInfo.tabId;
	
	if(tabId === "undefined")
	{
		return;
	}
	
	AddToAutoTabList(tabId);
}); 

chrome.windows.onCreated.addListener(function(window) {
	var tabs = window.tabs;	
	if(!tabs)
	{
		return;
	}
	
	var tab = tabs[0];
	var tabId = tab.Id;
	
	if(tabId === "undefined")
	{
		return;
	}
	
	AddToAutoTabList(tabId);
});


function AddToAutoTabList(tabId)
{
	var loc = finalURLsList.indexOf(tabId);	
	if(loc != -1)			
	{
		//Swapping tabs so that the active tab always stay top 
		// of the stack
		if(tabId == finalURLsList[0])
		{	
			var temp = finalURLsList[1];		
			finalURLsList[1] = tabId;
			finalURLsList[0] = temp;
			return;
		}
	}
	
	if(currentBrowserActionState == "Open")
	{
		finalURLsList.push(tabId);		
		
		if(finalURLsList.length == 2)
		{
			currentBrowserActionState = "Auto";		
			SetLockedBrowserActionState();		
		}		
	}
	else if (currentBrowserActionState == "Auto")
	{
		if(finalURLsList.length >=2)
		{
			finalURLsList.shift();
		}
		
		finalURLsList.push(tabId);		
	}
}



function SetLockedBrowserActionState()
{
	chrome.browserAction.setIcon(
			{path: searching_images[0]}, function(){				
	});
	
	chrome.browserAction.setPopup(
		{ popup: ''});
}

function SetOpenBrowserActionState()
{
	chrome.browserAction.setIcon(
			{path: searching_images[1]}, function(){				
	});
	
	chrome.browserAction.setPopup(
		{ popup: 'popup.html'});
}

chrome.browserAction.onClicked.addListener(function(tab)
{
	if((currentBrowserActionState == "Locked") || (currentBrowserActionState == "Auto"))
	{
		finalURLsList = new Array();
		currentBrowserActionState = "Open";
		SetOpenBrowserActionState();	
	}
	else
	{
		currentBrowserActionState = "Locked";		
		SetLockedBrowserActionState();		
	}
});

chrome.runtime.onMessage.addListener( function(request,sender,sendResponse)
{
	finalURLsList = request.data;		
	SetLockedBrowserActionState();
	currentBrowserActionState = "Locked";
});  

var finalURLsList = new Array();
var currentTabID = -1;
var currentBrowserActionState = "Open";
var searching_images = ['locked.png',
                        'open.png'];
 var numTabsOpen = 0;