from django.contrib import admin
from zipsearch.models import ZipCodeEntry

class ZipAdmin(admin.ModelAdmin):
    list_display = ('zipcode', 'latitude', 'longitude', 'city_name', 'state')
    list_filter = ('city_name', 'state')

admin.site.register(ZipCodeEntry, ZipAdmin)
