from django.http import HttpResponse
from zipsearch.models import ZipCodeEntry

def lookup(request):
    for code in ['10270',]:
        z = ZipCodeEntry.within_radius(code)
        print z
    return HttpResponse(str(z))
