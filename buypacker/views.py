from association.models import Association
from buypacker.models import CompteBancaire

# Create your views here.
@login_required
def nouvel_evenement(request, association_pseudo):
	association = get_object_or_404(Association, pseudo = association_pseudo)
	compte = get_object_or_404(CompteBancaire, association = association)
	return render_to_response('buypacker/nouveau.html', {'association':association, 'comptebancaire':comptebancaire},context_instance=RequestContext(request))