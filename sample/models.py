from django.db import models

# Simple example model

class City(models.Model):
    COUNTRIES = (
        ('uk', 'United Kingdom'),
        ('de', 'Germany',),
        ('fr', 'France'),
        ('ie', 'Ireland'),
    )
    name = models.CharField(max_length=100)
    country = models.CharField(choices=COUNTRIES, max_length=2)

