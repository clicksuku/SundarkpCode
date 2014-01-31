chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    chrome.pageAction.show(tabId);
    chrome.pageAction.setTitle({
        tabId: tab.id,
        title: 'url=' + tab.url
    });
});