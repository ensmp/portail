//VOTE AU SONDAGE
/*	$(function() {
		$("#vote1form").submit(function(){
			choix = 1;
			csrfmiddlewaretoken = $(this).find("input[name=csrfmiddlewaretoken]").val();	
			$.post("/sondages/voter/", {choix:choix, csrfmiddlewaretoken:csrfmiddlewaretoken},
				function(data) {
					alert(data);					
				}
			);
			return false;
		});
	});*/
// CLIC PRECEDENT

$(document).ready(function() {
	var aujourdhui = new Date();
	var jour = aujourdhui.getDate();
    var mois = aujourdhui.getMonth()+1;
    if (jour < 10) {
		jour = '0' + jour;
	}
	if (mois < 10) {
		mois = '0' + mois;
	}
	$("#sondage_date").prepend(jour + '/' + mois + '/' + aujourdhui.getFullYear() + ' ');
	$("#barre_reponse_1").progressBar({steps : 0});
	$("#barre_reponse_2").progressBar({steps : 0});
	$("#sondage_suivant").hide();
});

$(function() {



	$("#sondage_precedent").click(function(){
		jours_depuis++;
		$.getJSON('/sondages/'+jours_depuis+'/json/', function(data){
			$("#sondage_date").text(data.date_parution + ' ('+(data.nombre_reponse_1+data.nombre_reponse_2) + ' vote' + ((data.nombre_reponse_1+data.nombre_reponse_2>1)?'s)':')'));
			$("#sondage_question").text(data.question);
			$("#texte_reponse_1").text(data.reponse1);
			$("#texte_reponse_2").text(data.reponse2);			
			if (data.nombre_reponse > 0) {
				$('#barre_reponse_1').progressBar(Math.round((100*data.nombre_reponse_1)/data.nombre_reponse), {steps : 20});
				$('#barre_reponse_2').progressBar(Math.round((100*data.nombre_reponse_2)/data.nombre_reponse), {steps : 20});
			}
			else{
				$('#barre_reponse_1').progressBar(0);
				$('#barre_reponse_2').progressBar(0);
			}
			$("#sondage_suivant").show();
			if (data.is_dernier) $("#sondage_precedent").hide();
		}).error(function() {jours_depuis--; });
	});
	$("#sondage_suivant").click(function(){
		jours_depuis--;
		$.getJSON('/sondages/'+jours_depuis+'/json/', function(data){
			$("#sondage_date").text(data.date_parution + ' ('+(data.nombre_reponse_1+data.nombre_reponse_2) + ' vote' + ((data.nombre_reponse_1+data.nombre_reponse_2>1)?'s)':')'));
			$("#sondage_question").text(data.question);
			$("#texte_reponse_1").text(data.reponse1);
			$("#texte_reponse_2").text(data.reponse2);
			if (data.nombre_reponse > 0) {
				$('#barre_reponse_1').progressBar(Math.round((100*data.nombre_reponse_1)/data.nombre_reponse), {steps : 20});
				$('#barre_reponse_2').progressBar(Math.round((100*data.nombre_reponse_2)/data.nombre_reponse), {steps : 20});
			}
			else{
				$('#barre_reponse_1').progressBar(0);
				$('#barre_reponse_2').progressBar(0);
			}
			$("#sondage_precedent").show();
			if (data.is_premier) $("#sondage_suivant").hide();
		}).error(function() {jours_depuis++; });
	});
});
