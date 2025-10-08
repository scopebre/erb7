from django.shortcuts import render
from listings.models import Listing
from doctors.models import Doctor
from listings.choices import district_choices, room_choices, night_choices
#from django.http import HttpResponse

# Create your views here.
def index(request):
    #return render("<h1>Hello, world!</h1")
    #print(request.path)
    #print(request)
    listings = Listing.objects.filter(is_published=True)[:3] #get the 3 most recent listings
    context = {"listings":listings,
               "district_choices":district_choices,
               "room_choices":room_choices,
               "night_choices":night_choices,
              }
    return render(request,'pages/index.html',context)

def about(request):
    #print(request)
    doctors = Doctor.objects.order_by('-hire_date')[:3] #get the 3 most recent doctors
    mvp_doctors = Doctor.objects.all().filter(is_mvp=True) #get all mvp doctors
    context = {
                "doctors":doctors,
                "mvp_doctors":mvp_doctors
             }
    return render(request,'pages/about.html',context)