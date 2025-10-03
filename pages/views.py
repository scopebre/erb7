from django.shortcuts import render
from listings.models import Listing
#from django.http import HttpResponse

# Create your views here.
def index(request):
    #return render("<h1>Hello, world!</h1")
    #print(request.path)
    #print(request)
    listings = Listing.objects.filter(is_published=True)[:3] #get the 3 most recent listings
    context = {"listings":listings}
    return render(request,'pages/index.html',context)

def about(request):
    #print(request)
    return render(request,'pages/about.html')