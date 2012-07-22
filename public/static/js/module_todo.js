//ENVOI D'UNE NOUVELLE NOTE
	$(function() {
		$("#todoform").submit(function(){
			note = $(this).find("input[name=note]").val();
			csrfmiddlewaretoken = $(this).find("input[name=csrfmiddlewaretoken]").val();	
			$.post("/todo/nouveau", {note:note, csrfmiddlewaretoken:csrfmiddlewaretoken},
				function(data) {
					//alert(data);
					$("#liste_notes").append('<li><a href = "/todo/'+0+'/supprimer/">'+note+'</a></li>');
				}
			);
			return false;
		});
	});
	
	$(function() {
		$("#todoform a").clicked(function(){
			alert("click");
		});
	});