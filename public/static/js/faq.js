$(document).ready(function(){
	
	/** SLIDE DU MESSAGE */
	$(".objet").click(function(){	
		var contenu = $(this).closest(".objet").next();
		if (contenu.is(':visible')){			
			contenu.slideUp(500); 						
		}		
		else{
			contenu.slideDown(500); 			
		}
	});
	
	/** LANCEMENT DU SITE */
	$(".question").hide();  //onload	
});