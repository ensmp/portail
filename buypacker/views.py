#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from association.models import Association
from buypacker.models import CompteBancaire, CompteBancaireForm

schoolExtendId = 35
schoolExtendSecret = '8PVbdlGiFFMQK6OVDV6s7sdzSbRuMpBTzqAGT4f9'

@login_required
def nouvel_evenement(request, association_pseudo):
	association = get_object_or_404(Association, pseudo = association_pseudo)
	try:
		comptebancaire = CompteBancaire.objects.get(association = association)
	except CompteBancaire.DoesNotExist:
		return redirect(association.get_absolute_url()+'comptebancaire/modifier/')
	# Les données transmises à BuyPacker pour la création de l'événement
	data = {'vendorExtendId':association.pseudo, 'vendorName':association.nom}
	# Génération du formulaire
	dataForm = sendDataForm('http://beta.buypacker.com/deal/nouveau', data)
	return render_to_response('buypacker/nouveau.html', {'association':association, 'comptebancaire':comptebancaire, 'dataForm':dataForm},context_instance=RequestContext(request))

def modifier_compte_bancaire(request, association_pseudo):
	association = get_object_or_404(Association, pseudo = association_pseudo)
	try:
		comptebancaire = CompteBancaire.objects.get(association=association)
	except CompteBancaire.DoesNotExist:
		comptebancaire = CompteBancaire(association=association)
	if request.method == 'POST':
		form = CompteBancaireForm(request.POST, instance=comptebancaire)
		if form.is_valid():
			form.save()
		return redirect(association)
	else:
		form = CompteBancaireForm(instance=comptebancaire)
		return render_to_response('buypacker/compteBancaire.html', {'form': form,}, context_instance=RequestContext(request))
		
		
	

def sendDataForm(endpoint, data, method = 'POST'):
	# Iframe BuyPacker
	response = getIframe(endpoint)
	# Début du formulaire
	response += '<form action="' + endpoint + '" method="' + method + '" id="BuyPackerForm" target="BuyPackerIframe">'
	# Sécurité
	security = hash(data)
	print security['schoolExtendHash']
	response += '<input type="hidden" name="schoolExtendTime" value="' + security['schoolExtendTime'] + '"/>'
	response += '<input type="hidden" name="schoolExtendHash" value="' + security['schoolExtendHash'] + '"/>'
	response += '<input type="hidden" name="schoolExtendId" value="' + str(security['schoolExtendId']) + '"/>'
	# Les données
	response += '<textarea name="schoolExtendData" style="display: none">' + security['schoolExtendData'] + '</textarea>'
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
	if endpoint == '':
		response += '<iframe name="BuyPackerIframe" id="BuyPackerIframe" src="about:blank" width="740px" height="500px" frameborder="0px" scrolling="no" style="border: 0px;"></iframe>'
	else:
		response += '<iframe name="BuyPackerIframe" id="BuyPackerIframe" src="' + endpoint + '?schoolExtendId=' + str(schoolExtendId) + '" width="740px" height="500px" scrolling="no" frameborder="0px" style="border: 0px;"></iframe>'
	# Retour de la fonction
	return response;

def hash(data, currentTime = ''):
	# Timestamp
	import time
	if currentTime == '':
		currentTime = int(time.mktime(time.localtime()))
	# Encodage en JSON
	import json
	data = json.dumps(data)
	#Hashage
	import hmac
	import hashlib
	import base64
	print str(currentTime) + data
	data_hash = hmac.new(schoolExtendSecret, msg = str(currentTime) + data, digestmod=hashlib.sha256).hexdigest()
	#base64.b64encode(dig).decode()
	# Retour de la réponse
	return {
		'schoolExtendTime'	: str(currentTime),
		'schoolExtendHash'	: data_hash,
		'schoolExtendId'	: schoolExtendId,
		'schoolExtendData'	: data
	}