var newpl = null;

$(document).ready(function() {	
	
	registerHandlebarHelpers();
	$("#includedContent").load("Card.html");

	var id  = ChannelData[0]['id'];
	var playlists = ChannelData[0]['playlists'];
	newpl = sortPl(playlists);
	var title  = ChannelData[0]['title'];
	initializeSidebar(newpl);
});

function registerHandlebarHelpers()
{
	Handlebars.registerHelper('if_eq', function(a, b, opts) {
    if(a == b) // Or === depending on your needs
        return opts.fn(this);
    else
        return opts.inverse(this);
	});	
}


function sortPl(playlists)
{
	var newpl = playlists.sort(function(first, second) {
	    var a = first.title;
	    var b = second.title;
	    
	    if(a > b) {
	        return 1;
	    } else if(a < b) {
	        return -1;
	    } else {
	        return 0;
	    }
	});	

	return newpl;
}

function initializeSidebar(newpl)
{
	var map = {};
	
	$('#sidebar').w2sidebar
	({
			name: 'sidebar',
	        nodes: [
			            { id: 'level-channels', text: 'Channels', expanded: true, group: true }
		            ],
            onClick: function(event){
            	PopulateVideos(event,map);
            }

	});	

	for( var i=0, l=newpl.length; i<l; i++ ) 
	{
		    w2ui.sidebar.insert('level-channels', null, [
	    		{ id: newpl[i].id, text: newpl[i].title }
		    ]);	

    		map[newpl[i].id] = newpl[i];
	}
}



function PopulateVideos(event, map) 
{
    var pl = map[event.target]

	var videos = JSON.parse(JSON.stringify({"video": pl.videos}));    
	var theTemplateScript = $("#card-template").html();
    
    // Compile the template
  	var theTemplate = Handlebars.compile(theTemplateScript);
    // This is the default context, which is passed to the template
  	var context = videos;
	
	// Pass our data to the template
    var theCompiledHtml = theTemplate(context);
	$("#Cards").html(theCompiledHtml);

}


function exportDataTemplate()
{
	var playlists = JSON.parse(JSON.stringify({"playlists": newpl}));    
	var theTemplateScript = $("#export-template").html();
    
    // Compile the template
  	var theTemplate = Handlebars.compile(theTemplateScript);
    // This is the default context, which is passed to the template
  	var context = playlists;
	
	// Pass our data to the template
    var theCompiledHtml = theTemplate(context);
	var blob = new Blob([theCompiledHtml], {type: "text/plain;charset=utf-8"});
	saveAs(blob, "Channels.html");
}



