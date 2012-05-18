from django.shortcuts import redirect
from todo.models import Todo
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def nouveau(request):
	if request.method == 'POST':
		#update_profile(request,mineur_login,phone=request.POST['phone'],promo=request.POST['promo'],chambre=request.POST['chambre'],option=request.POST['option'])
		Todo.objects.create(eleve = request.user.get_profile(), contenu = request.POST['note'], date = datetime.now())
	return redirect('/messages')