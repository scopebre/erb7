from django.shortcuts import render
from django.http import HttpResponse
from .models import Listing

# Create your views here.

# def index(request):
#    return HttpResponse("<h1>Hello World!</h1>")

def listings(request):
    listings = Listing.objects.all()
    context = {"listings":listings}
    return render(request, 'listings/listings.html',context)

def listing(request):
    return render(request, 'listings/listing.html')

def search(request):
    return render(request, 'listings/search.html')
