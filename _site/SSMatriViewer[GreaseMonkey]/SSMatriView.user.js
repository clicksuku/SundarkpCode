// ==UserScript==
// @name        SSMatriView
// @namespace   http://sundarkp.wordpress.com/
// @description Change Page Layout to display profile photos
// @include     http://ssmatri.net/setup/ProfileListview.asp?*
// @author		Sundara Kumar Padmanabhan
// @version     1
// @require		http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js
// ==/UserScript==


$('#front').ready(function(){
    	
	function ajaxFailure()
	{
		alert("oops something went wrong");  
	}	
	
	function complete(content, tdImages)
	{
		var img_array = [];
		var pattern = /\<img[\s]*src(.*)/gi;
		var matches_array = content.match(pattern);
				
		if(matches_array)
		{				

			for(i=0; i < matches_array.length;i++)
			{				
				var matchedURL = matches_array[i];																		
				var index = matchedURL.indexOf("\"");																		
				var URL = matchedURL.substring(index+1);						
				index = URL.indexOf("\"");
				URL = URL.substring(0,index);	
				img_array.push(URL);
			}		
						
			var imgElements = "";

			for(j=0; j < img_array.length;j++)
			{
				imgElements = imgElements + "<img src=\"" + img_array[j] + "\"></img>";
			}
								
			try
			{
				tdImages.empty();	
				tdImages.html(imgElements);				
			}
			catch(e)
			{
				alert(e);
			}
		}
	}

    function selectFocusTable(tables)
    {
        var $focusTable = tables.eq(2);		
		var link;
		var tbody;
		var tdImg;
		
        if($focusTable)
        {
            var trs = $focusTable.children("tbody").children("tr");
            var selectedTrs = trs.slice(4,54);
            
            var selectedTrs2 = selectedTrs.filter( function(){
                var img = $(this).find("img");     
                
                if(img.length > 0)                
                {                                               
                    return  true;
                }
            });
    			
            if(selectedTrs2)
            {                                                            
				selectedTrs2.each(function(index) {        
					link =  $(this).children().eq(1).find("a").attr("href"); 
					tbody = $(this).children().eq(2).find("tbody");
					tdImg = tbody.find("td").eq(1);	

					$.ajax({
						type: 'GET', 
						url:link,    
						dataType: 'html',
						cache:false,
						async: false,
						success:function(data)
						{					
							complete(data, tdImg);
							
						},
						error:ajaxFailure           
					});
                });			
				
				
            }              			    
        }		    
    }

    function selectTables()
    {			
        var tables = $("center").children("table");         
        selectFocusTable(tables);      
    }     

    selectTables();        
});

		