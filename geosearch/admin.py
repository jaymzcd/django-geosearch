from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from geosearch.models import GeoEntry, PostalCode

class GeoEntryAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'content_type', 'object_id')
    list_filter = ('content_type',)

class GeoEntryInline(GenericTabularInline):
    model = GeoEntry

class GeoAdmin(admin.ModelAdmin):
    """ Use this with your models that inherit GeoModel """
    inlines = [GeoEntryInline,]


admin.site.register(GeoEntry, GeoEntryAdmin)
admin.site.register(PostalCode, GeoAdmin)
