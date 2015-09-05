# -*- coding: utf-8 -*-
from association.models import Association, Adhesion
from mediamines.models import Photo, Gallery, PhotoEffect
from trombi.models import UserProfile
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate , login, logout
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage
from django.utils import simplejson
from datetime import datetime
import json
import urllib
from base64 import standard_b64encode
from Crypto.Cipher import AES

def connection(request):
    
    if request.method == 'POST':
        logi = request.POST["login"]
        mdp = request.POST["mdp"]
        user=authenticate(username=str(logi), password=str(mdp))
        if user is not None:
            login(request, user)
            return redirect('/sso/1y1b/authentication')
        else:
            return render_to_response('1y1b/login.html',context_instance=RequestContext(request)) 
    else:
        user = request.user
        if user.is_authenticated():
            profil = user.get_profile();
            response = HttpResponse(mimetype='application/json')
            user_infos = simplejson.dumps({
                'login': profil.user.username,
                'email':profil.user.email,
                'first_name': profil.first_name.title(),
                'last_name': profil.last_name.title(),
                'date':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
            #http://stackoverflow.com/questions/17834987/why-doesnt-it-work-when-using-python-to-encrypt-then-ruby-to-decrypt     
            ## sudo pip install pycrypto
            string_to_encode = user_infos
            def pad(x, n=16):
                p = n - (len(x) % n)
                return x + chr(p) * p
            key = "250ilwow5zo4jyw0"
            en = AES.new(key=key, mode=AES.MODE_CFB, IV="0" * 16, segment_size=128)
            cipher = en.encrypt(pad(string_to_encode))
            cipher64 = standard_b64encode(cipher)
            print cipher64
            user_infos=urllib.quote_plus(cipher64)
            if 'desired_page' in request.GET:
                desired_page= request.GET['desired_page']
                desired_page= urllib.quote_plus(desired_page)
                url='http://mines-paristech.1year1book.com/sso/callback?token='+user_infos+'&desired_page='+desired_page
            else:
                url='http://mines-paristech.1year1book.com/sso/callback?token='+user_infos
            print(url)
            return render_to_response('1y1b/redirect.html',{'url': url},context_instance=RequestContext(request)) 
        else: 
            return render_to_response('1y1b/login.html',context_instance=RequestContext(request)) 
            

        

def logout_view(request):
    logout(request)
    url= request.GET['page']
    return render_to_response('1y1b/redirect.html',{'url': url},context_instance=RequestContext(request)) 

#def yearbook(request):
#    url='http://mines-paristech.1year1book.com/'
#    return render_to_response('1y1b/redirect.html',{'url': url},context_instance=RequestContext(request)) 