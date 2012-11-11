from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from association.models import Association
from buypacker.models import CompteBancaire

SCHOOL_EXTEND_TIME = ''

@login_required
def nouvel_evenement(request, association_pseudo):
	association = get_object_or_404(Association, pseudo = association_pseudo)
	comptebancaire = get_object_or_404(CompteBancaire, association = association)
	data = {'vendorExtendId':association.pseudo, 'vendorName':association.pseudo}
	dataForm = sendDataForm('http://beta.buypacker.com/deal/nouveau', data)
	return render_to_response('buypacker/nouveau.html', {'association':association, 'comptebancaire':comptebancaire, 'dataForm':dataForm},context_instance=RequestContext(request))
	
def sendDataForm(endpoint, data, method = 'POST'):
	# Iframe BuyPacker
	response = getIframe(endpoint)
	# Début du formulaire
	response += '<form action="' + endpoint + '" method="' + method + '" id="BuyPackerForm" target="BuyPackerIframe">'
	# Sécurité
	security = self::hash(data)
	response += '<input type="hidden" name="schoolExtendTime" value="' + security.schoolExtendTime + '"/>'
	response += '<input type="hidden" name="schoolExtendHash" value="' + security.schoolExtendHash + '"/>'
	response += '<input type="hidden" name="schoolExtendId" value="' + security.schoolExtendId + '"/>'
	# Les données
	response += '<textarea name="schoolExtendData" style="display: none">' + $security.schoolExtendData + '</textarea>'
	# Fin du formulaire
	response += '</form>'
	# Soumission automatique du formulaire
	response += '<script type="text/javascript">document.getElementById("BuyPackerForm").submit();</script>';
	# Retour de la fonction
	return response
	
def getIframe(endpoint = ''):
	# Script de redimensionnement de l'iframe
	response = '<script type="text/javascript">function BuyPackerResize(height){document.getElementById("BuyPackerIframe").height = parseInt(height);}</script>'
	# Iframe
	if endpoint = '':
		response += '<iframe name="BuyPackerIframe" id="BuyPackerIframe" src="about:blank" width="740px" height="500px" frameborder="0px" scrolling="no" style="border: 0px;"></iframe>'
	else:
		response += '<iframe name="BuyPackerIframe" id="BuyPackerIframe" src="' + endpoint + '?schoolExtendId=' + schoolExtendId + '" width="740px" height="500px" scrolling="no" frameborder="0px" style="border: 0px;"></iframe>'
	# Retour de la fonction
	return response;

def hash(data, currentTime = ''):
	# Timestamp
	import time
	if currentTime == '':
		currentTime = time.localtime()
	# Encodage en JSON
	data = json_encode(data)
	# Retour de la réponse
	return {
		'schoolExtendTime'	: currentTime,
		'schoolExtendHash'	: hash_hmac('sha256', currentTime + data, schoolExtendSecret),
		'schoolExtendId'	: schoolExtendId,
		'schoolExtendData'	: data
	}