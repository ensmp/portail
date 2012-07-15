$(document).ready(function(){

	$("td.objet").click(function(){	
		if ($(this).parent().parent().parent().parent().next().is(':visible')){			
			$(this).parent().parent().parent().parent().next().slideUp(500); 						
		}		
		else{
			$(this).parent().parent().parent().parent().next().slideDown(500); 			
		}
	});
	
/*lancement du site*/
	$(".message_contenu").hide();  //onload	

});
