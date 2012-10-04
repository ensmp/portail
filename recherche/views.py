import re
from django.db.models import Q
from messages.models import Message
from trombi.models import UserProfile
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.


def search(request):
	query_string = ''
	found_messages = None
	found_users = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		message_query = get_query(query_string, ['objet', 'contenu'])
		user_query = get_query(query_string, ['first_name', 'last_name', 'phone', 'chambre', 'user__username'])
		found_messages = Message.objects.filter(message_query).order_by('-date')
		found_users = UserProfile.objects.filter(user_query).order_by('user__username')
		
		found_messages = found_messages.filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all()) | Q(association__in=request.user.get_profile().association_set.all()))
		
		if query_string.lower() == 'dieu':
			found_users = UserProfile.objects.filter(user__username = '11leuren')
			
	return render_to_response('recherche/resultats.html', { 'query_string': query_string, 'list_messages': found_messages, 'list_users': found_users }, context_instance=RequestContext(request))



def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query