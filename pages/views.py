from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.
def index(request):
    #return render("<h1>Hello, world!</h1")
    #print(request.path)
    #print(request)
    return render(request,'pages/index.html')

def about(request):
    #print(request)
    return render(request,'pages/about.html')