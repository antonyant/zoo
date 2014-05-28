from django.db import models
from photologue.models import Photo, Gallery


class GalleryType(models.Model):
    gallery_type = models.CharField(max_length=20)

    def __unicode__(self):
        return self.gallery_type


class GalleryOrder(models.Model):
    '''
    ** Photo Ordering **
    
    To use photo ordering *all* photos must re-included before.

    Default ordering will be used if no photos are included here.

    If any photos are included here this will override any photos in photologue version of gallery.

    ** Hero Image **

    If no hero image is specified the *first* image from the gallery will be used.
    '''
    active = models.BooleanField(default=True)
    gallery_type = models.ForeignKey(GalleryType, blank=True, null=True)
    gallery = models.ForeignKey(Gallery)
    order = models.IntegerField()
    hero_image = models.ForeignKey(Photo, blank=True, null=True)

    def __unicode__(self):
        return '%s -- %s' % (self.order, self.gallery)

    class Meta:
        ordering = ['-active', 'order']


class PhotoOrder(models.Model):
    gallery_order= models.ForeignKey(GalleryOrder)
    photo = models.ForeignKey(Photo, blank=True, null=True)
    order = models.IntegerField()    

    def __unicode__(self):
        return '%s -- %s' % (self.gallery_order, self.photo)

    class Meta:
        ordering = ['order']
