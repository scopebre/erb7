from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Listing
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator


# Create your views here.

# def index(request):
#    return HttpResponse("<h1>Hello World!</h1>")

def listings(request):
    # listings = Listing.objects.order_by('list_date').filter(is_published=True) #an alternative way to order by list_date descending
    # listings = Listing.objects.all()
    listings = Listing.objects.filter(is_published=True) #default ordering by list_date descending as defined in models.py
    paginator=Paginator(listings,3) #3 means every page show 3 items
    page=request.GET.get('page')
    paged_listings=paginator.get_page(page)
    context = {"listings":paged_listings}
    return render(request, 'listings/listings.html',context)

def listing(request,listing_id):
    # listing = Listing.objects.get(id=listing_id)
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {"listing":listing}
    return render(request, 'listings/listing.html',context)

def search(request):
    return render(request, 'listings/search.html')
