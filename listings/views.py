from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Listing
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from .choices import district_choices, room_choices, rooms_choices
from django.db.models import Q


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
    queryset_list = Listing.objects.order_by('-list_date')
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            # queryset_list = queryset_list.filter(description__icontains=keywords)
            queryset_list = queryset_list.filter(Q(description__icontains=keywords)|Q(title__icontains=keywords)|Q(doctor__name__icontains=keywords)|Q(services__name__icontains=keywords))
             #search in multiple fields, need to import Q from django.db.models
             #use distinct() to avoid duplicate results when a listing has multiple matching tags
             #iexact means case insensitive exact match
             #icontains means case insensitive contains match
             #startswith means starts with match
             #iendswith means ends with match
             #gt means greater than
             #gte means greater than or equal to
             #lt means less than
             #lte means less than or equal to
             #in means in a list of values, e.g. .filter(id__in=[1,2,3])
    if 'district' in request.GET:
        district = request.GET['district']
        if district:
            queryset_list = queryset_list.filter(district__iexact=district)     
    if 'rooms' in request.GET:
        rooms = request.GET['rooms']
        if rooms:
            queryset_list = queryset_list.filter(rooms__lte=rooms) #less than or equal to                   
    if 'room_type' in request.GET:
        room_type = request.GET['room_type']
        if room_type:
            queryset_list = queryset_list.filter(room_type__iexact=room_type)
    paginator=Paginator(queryset_list,3) #3 means every page show 3 items
    page=request.GET.get('page')
    paged_listings=paginator.get_page(page)
    context = {"listings":paged_listings,
                # "listings":queryset_list,
               "district_choices":district_choices,
               "rooms_choices":rooms_choices,
               "room_choices":room_choices,
               "values":request.GET,
               }            
    return render(request, 'listings/search.html', context)
