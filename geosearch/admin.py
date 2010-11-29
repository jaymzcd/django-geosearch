from django.contrib import admin
from geosearch.models import GeoEntry

class GeoEntryAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'content_type', 'object_id')
    list_filter = ('content_type',)

admin.site.register(GeoEntry, GeoEntryAdmin)
