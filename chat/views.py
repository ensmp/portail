# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

from models import Room, Message

import time

# The format of the date displayed in the chat window can be customised.
try:
    DATE_FORMAT = settings.JQCHAT_DATE_FORMAT
except:
    # Use default format.
    DATE_FORMAT = "H:i"

# How many messages to retrieve at most.
JQCHAT_DISPLAY_COUNT = getattr(settings, 'JQCHAT_DISPLAY_COUNT', 100) 

#------------------------------------------------------------------------------
@login_required
def window(request):
    """A basic chat client window."""

    ThisRoom = Room.objects.order_by('-created')[0] #get_object_or_404(Room, id=id)

    return render_to_response('chat/chat_test.html', {'room': ThisRoom},
                              context_instance=RequestContext(request))

#------------------------------------------------------------------------------
@login_required
def WindowWithDescription(request, id):
    """A variant of the basic chat window, includes an updatable description to demonstrate
    how to extend the chat system."""

    ThisRoom = get_object_or_404(Room, id=id)

    return render_to_response('chat/chat_test_with_desc.html', {'room': ThisRoom},
                              context_instance=RequestContext(request))

#------------------------------------------------------------------------------
class Ajax(object):
    """Connections from the jQuery chat client come here.

    We receive here 2 types of calls:
    - requests for any new messages.
    - posting new user messages.

    Any new messages are always returned (even if/when posting new data).

    Requests for new messages should be sent as a GET with as arguments:
    - current UNIX system time on the server. This is used so that the server which messages have
    already been received by the client.
    On the first call, this should be set to 0, thereafter the server will supply a new system time
    on each call.
    - the room ID number.
    
    Requests that include new data for the server (e.g. new messages) should be sent as a POST and 
    contain the following extra args:
    - an action code, a short string describing the type of data sent.
    - message, a string containing the message sent by the user.

    The returned data contains a status flag:
     1: got new data.
     2: no new data, nothing to update.

    This code is written as a class, the idea being that implementations of a chat window will 
    have extra features, so these will be coded as derived classes.
    Included below is a basic example for updating the room's description field.

    """

    # Note that login_required decorators cannot be attached here if the __call__ is to be overridden.
    # Instead they have to be attached to child classes.
    def __call__(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseBadRequest('You need to be logged in to access the chat system.')
    
        StatusCode = 0 # Default status code is 0 i.e. no new data.
        self.request = request
        try:
            self.request_time = int(self.request.REQUEST['time'])
        except:
            return HttpResponseBadRequest("What's the time?")
        self.ThisRoom = Room.objects.get(id = id)
        NewDescription = None

        if self.request.method == "POST":
            # User has sent new data.
            action = self.request.POST['action']
    
            if action == 'postmsg':
                msg_text = self.request.POST['message'].replace("\\", "\\\\")
                msg_text = ' '.join(msg_text.split())
                
                if len(msg_text.strip()) > 0: # Ignore empty strings.
                    Message.objects.create_message(self.request.user, self.ThisRoom, msg_text)
        else:
            # If a GET, make sure that no action was specified.
            if self.request.GET.get('action', None):
                return HttpResponseBadRequest('Need to POST if you want to send data.')

        # If using Pinax we can get the user's timezone.
        try:
            user_tz = self.request.user.account_set.all()[0].timezone
        except:
            user_tz = settings.TIME_ZONE
    
        # Extra JSON string to be spliced into the response.
        CustomPayload = self.ExtraHandling()
        if CustomPayload:
            StatusCode = 1
    
        # Get new messages - do this last in case the ExtraHandling has itself generated
        # new messages. 

        NewMessages = Message.objects.filter(unix_timestamp__gt=self.request_time).order_by('-id')[:JQCHAT_DISPLAY_COUNT]
        if NewMessages:
            StatusCode = 1
            NewMessages = reversed(NewMessages)
   
        response =  render_to_response('chat/chat_payload.json',
                                  {'current_unix_timestamp': int(time.time()),
                                   'NewMessages': NewMessages,
                                   'StatusCode': StatusCode,
                                   'NewDescription': NewDescription,
                                   'user_tz': user_tz,
                                   'CustomPayload': CustomPayload,
                                   'TimeDisplayFormat': DATE_FORMAT
                                   },
                                  context_instance=RequestContext(self.request))
        response['Content-Type'] = 'text/plain; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response

    def ExtraHandling(self):
        """We might want to receive/send extra data in the Ajax calls.
        This function is there to be overriden in child classes.
        
        Basic usage is to generate the JSON that then gets spliced into the main JSON 
        response.
        
        """
        return None
        

BasicAjaxHandler = Ajax()


#------------------------------------------------------------------------------
class DescriptionAjax(Ajax):
    """Example of how to handle calls with extra data (in this case, a room
    description field).
    """

    def ExtraHandling(self):
        # Check if new description sent.
        if self.request.method == "POST":
            action = self.request.POST['action']
            if action == 'change_description':
                # Note that we escape descriptions as a protection against XSS.
                self.ThisRoom.description = escape(self.request.POST['description'])
                self.ThisRoom.save()
                Message.objects.create_event(self.request.user, self.ThisRoom, 1)
        # Is there a description more recent than the timestamp sent by the client?
        # If yes, return an extra field to be tagged on to the JSON returned to the client.
        if self.ThisRoom.description and self.ThisRoom.description_modified > self.request_time:
            return ',\n        "description": "%s"' % self.ThisRoom.description
        
        return None

WindowWithDescriptionAjaxHandler = DescriptionAjax()
