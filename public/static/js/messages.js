$(document).ready(function(){
	
	/** SLIDE DU MESSAGE */
	$("td.objet").click(function(){	
		var contenu = $(this).closest(".message_infos").next();
		if (contenu.is(':visible')){			
			contenu.slideUp(500); 						
		}		
		else{
			contenu.slideDown(500); 			
		}
	});
	
	/** ENVOI DU COMMENTAIRE */
	$("textarea").keydown(function(e){
    // Enter was pressed without shift key
		if (e.keyCode == 13 && !e.shiftKey)
		{
			e.preventDefault();
			var form = $(this).closest("form")
			//form.submit();
			
			
			csrfmiddlewaretoken= form.find("input[name=csrfmiddlewaretoken]").val();
			comment = form.find("textarea[name=comment]").val();
			content_type = form.find("input[name=content_type]").val();
			object_pk = form.find("input[name=object_pk]").val();
			timestamp = form.find("input[name=timestamp]").val();
			security_hash = form.find("input[name=security_hash]").val();
			$.post("/comments/post/", {csrfmiddlewaretoken:csrfmiddlewaretoken, comment:comment, content_type:content_type, object_pk:object_pk, timestamp:timestamp, security_hash:security_hash},
				function(data) {
					form.find("textarea[name=comment]").val('');
					var comments = form.closest(".comment_form").prev();
					comments.append(data);
					comments.find(".comment:last").hide();
					comments.find(".comment:last").fadeIn("slow");
				}
			);
		}
	});
	
	/**FAVOURITE**/
	$('a.comment_delete img').hover(function() {
		$(this).attr({'src':'/static/comment_delete_hover.png'});
	},function() {
		$(this).attr({'src':'/static/comment_delete.png'});
	});
	
	/***  CLICK ***/
	$('a.comment_delete').click(function(e) {
		e.preventDefault();
		var commentaire = $(this).closest(".comment");
		csrfmiddlewaretoken= commentaire.find("input[name=csrfmiddlewaretoken]").val();
		comment_id= commentaire.find("input[name=comment_id]").val();
		$.post("/comments/delete/", {csrfmiddlewaretoken:csrfmiddlewaretoken, comment_id:comment_id},
				function(data) {					
					if (data === "deleted") {
						commentaire.fadeOut("slow");
					}
				}
			);
	});
	
	/** LANCEMENT DU SITE */
	$(".message_contenu").hide();  //onload	
	$('textarea').autosize();
});