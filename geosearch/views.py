from django.http import HttpResponse
from geosearch.models import GeoEntry

def lookup(request):
    for code in ['10270',]:
        z = GeoEntry.within_radius(code)
        print z
    return HttpResponse(str(z))
