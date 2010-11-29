from django.http import HttpResponse
from geosearch.models import GeoEntry
from decimal import Decimal
import json

def get_params(request, var='POST'):
    data = getattr(request, var)
    try:
        latitude = data['latitude']
        longitude = data['longitude']
        return [Decimal(latitude), Decimal(longitude)]
    except KeyError:
        return None
    except decimal.InvalidOperation:
        return None



def lookup(request):
    if request.POST:
        lat_long = get_params(request)
    elif request.GET:
        lat_long = get_params(request, 'GET')
    else:
        return HttpResponse(json.dumps({'error': 'BadRequest'}))
    if lat_long:
        z = GeoEntry.within_radius(lat_long, radius=250)
        return HttpResponse(json.dumps(z, sort_keys=False, indent=4))
    else:
        return HttpResponse(json.dumps({'error': 'NoRequest'}))
