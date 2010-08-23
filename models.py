from django.db import models
import math

class ZipCodeEntry(models.Model):
    """ Holds zipcode location data. This is based off the col's in
    the file via: http://www.populardata.com/zipcode_database.html
    The forumlas are based off nautical mile distances converted to
    radians so we need to convert *miles* to these n.miles. """

    zipcode = models.CharField(max_length=5)
    latitude = models.DecimalField(decimal_places=6, max_digits=9)
    longitude = models.DecimalField(decimal_places=6, max_digits=9)
    city_name = models.CharField(max_length=25)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=25)
    format = models.CharField(max_length=50)

    def __unicode__(self):
        return self.zipcode

    def distance_to_latlong(self, latlong):
        """ Returns the distance (in miles) of a zipcode's lat/long to
        a given target lat/long. This is basically a conversion of the
        javascript here: http://www.movable-type.co.uk/scripts/latlong.html """

        EARTH_RADIUS = 3440.07 # in n.miles
        NAUTICAL_TO_MILE_CONV = 1.15077945 # convert n.miles back to miles

        d_lat =  ZipCodeEntry.degrees_to_radians(latlong[0] - self.latitude)
        d_long =  ZipCodeEntry.degrees_to_radians(latlong[1] - self.longitude)
        source_lat = ZipCodeEntry.degrees_to_radians(latlong[0])
        target_lat = ZipCodeEntry.degrees_to_radians(self.latitude)

        hv_a = math.sin(d_lat/2)*math.sin(d_lat/2) + math.cos(source_lat)*math.cos(target_lat)*\
            math.sin(d_long/2)*math.sin(d_long/2)
        hv_c = 2*math.atan2(math.sqrt(hv_a), math.sqrt(1-hv_a))
        hv_distance = EARTH_RADIUS * hv_c

        return hv_distance * NAUTICAL_TO_MILE_CONV

    @staticmethod
    def degrees_to_radians(value):
        """ Returns a Lat/Long degree value to radian equivilant """
        return float(value)*math.pi/180.0

    @staticmethod
    def radians_to_degrees(value):
        return value*180.0/math.pi

    @staticmethod
    def miles_to_radians(value):
        """ Returns the radian value of a mile value. We need to convert
        to nautical miles first as the formula's use those """
        NAUTICAL_MILE_CONV = 0.868976 # convert miles to nautical miles
        nmiles = float(value)*NAUTICAL_MILE_CONV
        return nmiles*math.pi/(180.0*60.0)

    @staticmethod
    def calculate_latitude(source_lat, distance, heading):
        """ Calculates the latitude for a source point given a certain
        distance and heading direction. Values are in radians """
        return math.asin(math.sin(source_lat)*math.cos(distance) + \
            math.cos(source_lat)*math.sin(distance)*math.cos(heading))

    @staticmethod
    def calculate_longitude(prior_lat, source_long, distance, heading):
        """ Caclulated the longitude of a point. You *MUST* supply the
        (precalculted) latitude for the target point, so this call should
        always come after calculate_latitude """

        return ((source_long - \
            math.asin(math.sin(heading)*math.sin(distance)/math.cos(prior_lat))
            + math.pi) % (2*math.pi)) - math.pi

    @staticmethod
    def within_radius(_zipcode, radius=5):
        """ Takes an input zip & desired radius, works out the square
        (not circular) boundry box for it and returns the zip codes
        which fall within it. The method itself is outlined here:
            http://www.codeproject.com/KB/cs/zipcodeutil.aspx

        With lots of detail on the calculations here:
            http://mathforum.org/library/drmath/view/51816.html.

        The radius parameter is specified in *miles*. It's then
        converted into nautical miles & radians for further
        calculations.

        The actual query filters based on a box around the point, not
        a circle. So the end result is the area is around 22% larger
        than the "true" size. This can be further filtered on thesclient
        side or in the views rather than creating a complicated
        query. For most searches it's probably not a major problem
        in any case. """

        # These are our 4 points (N/S/E/W) We use this to build a bounding box
        HEADINGS = enumerate([0, math.pi/2, math.pi, 3*math.pi/2])

        try:
            zipcode = ZipCodeEntry.objects.get(zipcode=_zipcode)
        except ZipCodeEntry.DoesNotExist:
            # Maybe handle more gracefully?
            raise Exception('No zipcode matching query')

        source_lat = ZipCodeEntry.degrees_to_radians(zipcode.latitude)
        source_long = ZipCodeEntry.degrees_to_radians(zipcode.longitude)
        distance = ZipCodeEntry.miles_to_radians(radius)

        boundries = []

        for (cnt, heading) in HEADINGS:
            target_lat = ZipCodeEntry.calculate_latitude(source_lat, distance, heading)
            target_long = ZipCodeEntry.calculate_longitude(target_lat, source_long, distance, heading)

            boundries.append([ZipCodeEntry.radians_to_degrees(target_lat), \
                ZipCodeEntry.radians_to_degrees(target_long)])

        zipcodes = ZipCodeEntry.objects.all().filter(latitude__lte=str(boundries[0][0]),
            latitude__gte=str(boundries[2][0]), longitude__gte=str(boundries[1][1]),
            longitude__lte=str(boundries[3][1]))

        code_data = list()
        for code in zipcodes:
            code_data.append(dict(zipcode=code.zipcode, \
                distance=code.distance_to_latlong((zipcode.latitude, zipcode.longitude)))
            )

        return code_data

