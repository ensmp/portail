#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from trombi.models import UserProfile, Question, Reponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404, HttpResponse
import json
import os

@login_required
def page2048(request):

    return render_to_response('2048/2048.html', context_instance = RequestContext(request))