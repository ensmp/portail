$(function() {
	$('#messages').delay(5000).fadeOut();
});

 $(document).ready(function(){  
      
        $("ul.subnav").parent().append("<span class=\"fleche\"></span>");
		$("ul.topnav li ").hover(function() { 
      
            $(this).find("ul.subnav")/*.slideDown('fast')*/.show();
      
            $(this).hover(function() {  
            }, function(){  
                $(this).find("ul.subnav")/*.slideUp('slow')*/.hide();
            });  
      
            
            }).hover(function() {  
                $(this).addClass("subhover");
            }, function(){  
                $(this).removeClass("subhover"); 
        });
      
    });  