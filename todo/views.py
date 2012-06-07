from django.shortcuts import render_to_response, redirect
from todo.models import Todo
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse


# Create your views here.

@login_required
def nouveau(request):
	if request.method == 'POST':
		#update_profile(request,mineur_login,phone=request.POST['phone'],promo=request.POST['promo'],chambre=request.POST['chambre'],option=request.POST['option'])
		Todo.objects.create(eleve = request.user.get_profile(), contenu = request.POST['note'], date = datetime.now())
	return render_to_response('messages/action.html', {},context_instance=RequestContext(request))
	

def xhr_test(request):
    if request.is_ajax():
        if request.method == 'GET':
            message = "This is an XHR GET request"
        elif request.method == 'POST':
            message = "This is an XHR POST request"
            # Here we can access the POST data
            print request.POST
    else:
        message = "No XHR"
    return HttpResponse(message)