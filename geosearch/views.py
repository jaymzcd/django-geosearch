from django.http import HttpResponse
from geosearch.models import GeoEntry

def lookup(request):
    z = GeoEntry.within_radius([0, 0])
    print z
    return HttpResponse(str(z))
