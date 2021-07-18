from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

from .models import Watchlist
# Create your views here.

from PIL import Image
import base64
import numpy as np
import cv2
import io
# img = Image.open(r"C:\Users\Maus\Pictures\ProfilewFrame.jpg")

img = Image.open(r"account\static\img\img02.jpg")


def home(request):
    context = []

    person = {"name": "Lê Tuấn Anh", "id":17520237, "image":img}
    context.append(person)

    return render(request, "account/dashboard.html", {"context":context})

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	tasks = Watchlist.objects.all().order_by('-id')
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Watchlist.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()	
	img = serializer.data["image"]
	# print(type(img))
	base64_type = img.encode("utf-8")
	decoded_utf = base64.decodebytes(base64_type)
	byteImage = np.frombuffer(decoded_utf, dtype=np.uint8)
	
	frame = Image.open(io.BytesIO(byteImage))
	frame.show()
	
	# frame = cv2.imdecode(byteImage, flags=1)

	# cv2.imshow("Image", frame)
	# cv2.waitKey(0)

	# return Response(serializer.data)
	return Response('Item succsesfully created!')



@api_view(['POST'])
def taskUpdate(request, pk):
    task = Watchlist.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
    	serializer.save()
    
    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    Watchlist.objects.get(id=pk).delete()   
    return Response('Item succsesfully delete!')