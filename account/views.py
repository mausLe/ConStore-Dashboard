from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.





def home(request):
    return render(request, "account/dashboard.html")

def sync(request): 
    return HttpResponse("Sync Page")
