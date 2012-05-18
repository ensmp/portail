$(function() {
	$('#messages').delay(5000).fadeOut();
});

 $(document).ready(function(){  
      
        $("ul.subnav").parent().append("<span class=\"fleche\"></span>");
      /*
        $("ul.topnav li span.fleche").hover(function() { 
      
            $(this).parent().find("ul.subnav").slideDown('fast').show();
      
            $(this).parent().hover(function() {  
            }, function(){  
                $(this).parent().find("ul.subnav").slideUp('slow');
            });  
      
            
            }).hover(function() {  
                $(this).addClass("subhover");
            }, function(){  
                $(this).removeClass("subhover"); 
        });  */
		
		$("ul.topnav li ").hover(function() { 
      
            $(this).find("ul.subnav").slideDown('fast').show();
      
            $(this).hover(function() {  
            }, function(){  
                $(this).find("ul.subnav").slideUp('slow');
            });  
      
            
            }).hover(function() {  
                $(this).addClass("subhover");
            }, function(){  
                $(this).removeClass("subhover"); 
        });
      
    });  