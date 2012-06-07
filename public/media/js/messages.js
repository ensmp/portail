$(document).ready(function(){

/* initialisation */   
function initialisation(){
	$(".message_contenu").hide(); 	
}

/* Navigation */
/*
	$("td.objet").hover(function(){ 
		$("td.objet").css('cursor', 'pointer');
	});
*/
	
	$("td.objet").click(function(){	
		if ($(this).parent().parent().parent().parent().next().is(':visible')){			
			$(this).parent().parent().parent().parent().next().slideUp(500); 						
		}		
		else{
			$(this).parent().parent().parent().parent().next().slideDown(500); 			
		}
	});
	
	
/*lancement du site*/
	initialisation(); //onload	

});
