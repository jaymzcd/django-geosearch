#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# To run this you'll need to set two environment variables. Could probably do this
# as a management command but seems a bit messy since it's a very specific thing...
#
# export PYTHONPATH=/home/jaymz/development/www/vansemea
# export DJANGO_SETTINGS_MODULE=settings
#
# Obviously you'll need to change that path if you want to run it yourself

from locator.models import Dealer, City
from geosearch.models import GeoEntry
from base.models import Country
from django.db.models import Count

MAX_TOP_CITIES = 30 # how many of our "has the most dealers" to bin the others into
BOUNDRY_RADIUS = 25 # number of *miles* from our source point to include
CTYPES = {
    'dealer': 32,
    'city': 29,
}

for country in Country.objects.all():
    try:
        cities = Dealer.objects.values('city__pk', 'city__name') \
            .filter(country=country).annotate(Count('city')) \
            .order_by('-city__count')[:MAX_TOP_CITIES]
    except IndexError:
        print "No data for %s" % country.name

    print "Working out cities for %s\n" % country

    for city in cities[::-1]:
        # Look up the GeoEntry for this city. If we have one then we'll get
        # back a list of other enteries which are within BOUNDRY_RADIUS miles
        print "\nGetting db places within %dmiles of %s...\n" % (BOUNDRY_RADIUS, city['city__name'])

        try:
            primary_city = City.objects.get(pk=city['city__pk'], country=country)
            primary_city.primary_city = primary_city
            primary_city.save()
        except:
            "Could not find city matching %d and country id %d" % (city['city__pk'], country.pk)
            continue

        try:
            city_geoentry = GeoEntry.objects.get(content_type__pk=CTYPES['city'],
                object_id= city['city__pk'])
        except GeoEntry.DoesNotExist:
            print "No geoentry for %s" % city['city__name']
            continue

        radial_results = GeoEntry.within_radius(
            [city_geoentry.latitude, city_geoentry.longitude],
            BOUNDRY_RADIUS
        )

        # Trim off our source point, reverse and update our source cities
        # (we need to reverse it to have it assign by most populated last)
        for point in radial_results[1:][::-1]:
            if point['content_type'] == CTYPES['city']:
                source_city = City.objects.get(pk=point['object_id'])
                source_city.primary_city = primary_city
                source_city.save()
                print "Set %s as primary city for %s" % (primary_city, source_city)

