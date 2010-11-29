from django.db import models

# Simple example model

class City(models.Model):
    COUNTRIES = (
        ('uk', 'United Kingdom'),
        ('de', 'Germany',),
        ('fr', 'France'),
        ('ie', 'Ireland'),
    )
    name = models.CharField()
    country = models.CharField(choices=COUNTRIES)

