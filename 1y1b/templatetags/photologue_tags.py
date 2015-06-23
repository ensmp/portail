from django import template
from mediamines.models import Photo, Gallery
from datetime import datetime
register = template.Library()

@register.simple_tag
def next_in_gallery(photo, gallery):
    next = photo.get_next_in_gallery(gallery)
    if next:
        return '<a class = "mini_photo suivante" title="%s" href="%s"><img src="%s"/></a>' % (next.title, next.get_absolute_url(), next.get_thumbnail_url())
    return ""
    
@register.simple_tag
def previous_in_gallery(photo, gallery):
    prev = photo.get_previous_in_gallery(gallery)
    if prev:
        return '<a class = "mini_photo precedente" title="%s" href="%s"><img src="%s"/></a>' % (prev.title, prev.get_absolute_url(), prev.get_thumbnail_url())
    return ""

@register.simple_tag
def module_photo_url(user, index):
    if int(index)-1 < Photo.objects.all().count():        
        if user.get_profile().en_premiere_annee():    
            album = Gallery.objects.all().exclude(is_hidden_1A = True)[0]    
        else:
            album = Gallery.objects.all()[0]
        indice_depart = (137*datetime.now().day) % (album.photos.all().count()-5)
		
                
        photo = album.photos.all()[indice_depart + int(index)-1]
        return photo.get_module_url()
    else:
        return ''
