$(document).ready(function() {	
	
	$("#includedContent").load("Card.html");

	var id  = ChannelData[0]['id'];
	var playlists = ChannelData[0]['playlists'];

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

	Handlebars.registerHelper('if_eq', function(a, b, opts) {
    if(a == b) // Or === depending on your needs
        return opts.fn(this);
    else
        return opts.inverse(this);
	});

	var title  = ChannelData[0]['title'];
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

});


function PopulateVideos(event, map) 
{
    var pl = map[event.target]
	//alert(pl.id);

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

function exportData(ChannelData)
{

	var playlists = ChannelData[0]['playlists'];

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


	var html = [];
	
	html.push(
	  "<html>",
	  "<body>"
	);


	for( var i=0, l=newpl.length; i<l; i++ ) 
	{
    	html.push("<b>" + newpl[i].title + "</b> <ul type = \"circle\">");	
    	var videos = newpl[i].videos;

    	for( var j=0, len=videos.length; j<len; j++ ) 
		{	
			
			var title = videos[j].title;
			title = title.toLowerCase();

			if (title != "deleted video" ) {
    			html.push("<li><a href=https://www.youtube.com/watch?v="+ videos[j].id + "  target=\"_blank\">" + videos[j].title + "</a></li>");	
			}
			else
			{
				html.push("<li><font color=\"red\">Deleted Video</font><a href=https://www.google.co.in/search?q="+ videos[j].id + " target=\"_blank\">" + videos[j].id + "</a></li>");		
			}				
		}

		html.push("</ul><br/><br/>");	
	}

	html.push(
		"</body>",
		"</html>"
	);


	html =  html.join("");
	
	var blob = new Blob([html], {type: "text/plain;charset=utf-8"});
	saveAs(blob, "Channels.html");
}




