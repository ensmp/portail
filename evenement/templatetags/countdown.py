from django.template import Library, Node
import datetime
import time
     
register = Library()

@register.filter()
def countdown(value):
    start = datetime.date.today()
    end = datetime.date(*time.strptime(value,"%d/%m/%Y")[0:3])
    delta = end-start
    return delta.days