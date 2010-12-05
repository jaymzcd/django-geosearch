#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

from xml.dom import minidom
import MySQLdb
import urllib
import time

# Conf for the script follows
PK = 0
ADDRESS_FIELDS = [1, 2]
TABLE_NAME = 'vans_geocode'
API_KEY = 'ABQIAAAAWi-BMy_-pIul3fJ_Wtb0cRS-1g2Z1vGuftoTM8l-EvcBqLGZPhRinOd2yyL01ptA_B5BFkmNnB3yJg'

# Google Maps conf, see the following URL for info and how it works
# http://code.google.com/apis/maps/articles/phpsqlgeocode.html
MAP_URL = 'maps.google.com'
REQ_URL = 'http://%s/maps/geo?output=xml&key=%s' % (MAP_URL, API_KEY)
RATE_LIMIT = 5.76 # 15,000 req per day: 0.17 req per sec so 1 req every 5.76s

# Connect to our db and populate the cursor
db = MySQLdb.connect(user='', passwd='', db='')
curs = db.cursor()
exec_curs = db.cursor()
curs.execute("""SELECT * FROM %s""" % TABLE_NAME)

cnt = 0
while True:
    row = curs.fetchone()
    if row is None:
        break

    purty_address = ', '.join([row[field] for field in ADDRESS_FIELDS])
    query_address = urllib.urlencode(dict(q=purty_address))
    full_url = '%s&%s' % (REQ_URL, query_address)
    xml_data = urllib.urlopen(full_url)
    data = minidom.parse(xml_data)

    try:
        coords_tag = data.getElementsByTagName('coordinates')[0]
        coords = (coords_tag.childNodes[0].nodeValue).split(',')
        print u'%s is (%s, %s)' % (unicode(purty_address, 'utf-8'), coords[1], coords[0])
        exec_curs.execute("""UPDATE %s SET latitude="%s", longitude="%s", ok=1 WHERE id=%d""" \
            % (TABLE_NAME, coords[1], coords[0], row[PK]))
    except IndexError:
        print 'No coords returned for %s' % purty_address

    time.sleep(RATE_LIMIT) # rate limit
    cnt += 1
