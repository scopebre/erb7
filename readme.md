# Django Clinic Project
## Step to build the project
### 1. Create virtual environment
```bash
mkvirtualenv erb7
```
### 2. Create project folder
```bash
django-admin startproject erb7 .
```

```py
from django.shortcuts import render
from listings.models import Listing

#from django.http import HttpResponse

# Create your views here.
def index(request):
    listings = Listing.objects.filter(is_published=True)[:3] #get the 3 most recent listings
    context = {"listings":listings,
               "district_choices":district_choices,
               "room_choices":room_choices,
               "rooms_choices":rooms_choices,
              }
    return render(request,'pages/index.html',context)
```
