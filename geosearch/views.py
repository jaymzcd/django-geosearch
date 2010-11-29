from django.http import HttpResponse
from geosearch.models import GeoEntry
from decimal import Decimal
import json

def get_params(request, var='POST'):
    data = getattr(request, var)
    latlong = None
    radius = None
    fields = None
    try:
        latitude = data['latitude']
        longitude = data['longitude']
        latlong = [Decimal(latitude), Decimal(longitude)]
    except KeyError:
        pass
    except decimal.InvalidOperation:
        pass
    try:
        radius = data['radius']
    except KeyError:
        pass
    try:
        fields = list(data['fields'].split(','))
    except KeyError:
        pass
    return [latlong, radius, fields]



def lookup(request):
    if request.POST:
        lat_long, radius, fields = get_params(request)
    elif request.GET:
        lat_long, radius, fields = get_params(request, 'GET')
    else:
        return HttpResponse(json.dumps({'error': 'BadRequest'}))

    if lat_long and radius and fields:
        z = GeoEntry.within_radius(lat_long, radius, fields)
    elif lat_long and radius:
        z = GeoEntry.within_radius(lat_long, radius)
    elif lat_long:
        z = GeoEntry.within_radius(lat_long)
    else:
        return HttpResponse(json.dumps({'error': 'NoRequest'}))

    return HttpResponse(json.dumps(z, sort_keys=False, indent=4))

