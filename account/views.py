from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from PIL import Image
# img = Image.open(r"C:\Users\Maus\Pictures\ProfilewFrame.jpg")

img = Image.open(r"account\static\img\img02.jpg")




def home(request):
    context = []

    person = {"name": "Lê Tuấn Anh", "id":17520237, "image":img}
    context.append(person)

    return render(request, "account/dashboard.html", {"context":context})

def sync(request): 
    return HttpResponse("Sync Page")
