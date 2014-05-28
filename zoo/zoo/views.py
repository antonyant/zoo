from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

from gallery_orders.models import GalleryOrder
from photologue.models import Gallery, Photo


def galleries(request, tag, slug, context={}, template='photo/gallery_single.html'):
    '''

    ** Context **

    ``gallery`` -- gallery_order.GalleryOrder.gallery based on ``tag`` and ``slug``.

    ``photo_list`` -- could be one of two different lists
        - IF there are any photos at all under ``GalleryOrder`` these are used
        - otherwise the photos related to ``photologue.Gallery`` are used
    '''
    g = get_list_or_404(GalleryOrder, gallery__title_slug__contains=slug)[0]
    context['gallery_list'] = g
    p = g.photoorder_set.all()
    if p.count() != 0:
        q = []
        for x in p.order_by('order'): q.append(x.photo)
        context['photo_list'] = q
    else:
        context['photo_list'] = g.gallery.photos.all()
    return render_to_response(template, context_instance=RequestContext(request, context))

    
def galleries_tag(request, tag, context={}, template='photo/gall_ent.html'):
    '''

    ** Context **

    ``gallery_list`` -- gallery_order.GalleryOrder.gallery

    '''
    context['gallery_list'] = get_list_or_404(GalleryOrder, active=True, gallery_type__gallery_type=tag)
    return render_to_response(template, context_instance=RequestContext(request, context))




