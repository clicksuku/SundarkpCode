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
	var keys = Object.keys(finalURLsList).sort();
	
	if(finalURLsList.hasOwnProperty(currentTabID))	
	{
		var strCurrentId = String(currentTabID);
		var loc = keys.indexOf(strCurrentId);
		
		var nextTab = loc + 1;
		if(nextTab >= keys.length)
		{
			nextTab = 0;
		}						
	}
	else
	{
		nextTab = 0;
	}
	
	if(keys.length > 0)
	{
		nextTabId = keys[nextTab];
		chrome.tabs.update(parseInt(nextTabId), {"active":true,"highlighted":true}, function(tab){
			var window = tab.windowId;
			chrome.windows.update(window, {"focused":true});
		});
	}
}


chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) {
	if(finalURLsList.hasOwnProperty(tabId))	
	{
		delete finalURLsList[tabId];
		SwitchTabs();
	}
});

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
	if(currentBrowserActionState == "Locked")
	{
		finalURLsList = {};
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


var finalURLsList = {};
var currentTabID = -1;
var currentBrowserActionState = "Open";
var searching_images = ['locked.png',
                        'open.png'];
 