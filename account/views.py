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
import io
from django.db.models import Count
import itertools
from datetime import datetime
import glob
# img = Image.open(r"C:\Users\Maus\Pictures\ProfilewFrame.jpg")

# img = Image.open(r"static\img\img02.jpg")


def home(request):
	context = []

	tasks = Watchlist.objects.all().order_by('-id')
	serializer = TaskSerializer(tasks, many=True)
	#for item in serializer.data:
	#	print(item["name"])
	#print(len(serializer.data))
	tasks = Watchlist.objects.values('time').values('time')
	grouped0 = itertools.groupby(tasks, lambda d: d.get('time').strftime('%Y-%m-%d %H:%M:%S'))

	out0 = [(day[-8:], len(list(this_day))) for day, this_day in grouped0]
	out0 = out0[::-1]

	# print("OUT0: ", out0)
	grouped = itertools.groupby(tasks, lambda d: d.get('time').strftime('%Y-%m-%d'))

	out = [(day[-5:], len(list(this_day))) for day, this_day in grouped]
	out = out[::-1]
	data_length = 0
	
	for item in out:
		i1, i2 = item[0], item[1]
		data_length += i2

	date = []

	b1 = b2 = 0
	for item in out:
		i1, i2 = item[0], item[1]
		if b2 + i2 > data_length - 10:
			date.append((i1, i2 - (b2 + i2) + (data_length - 10)))
			break
		else:
			date.append((i1, i2))

	ctx = []
	address = glob.glob("static/img/img*.jpg")
	for i in range (0, len(serializer.data) - 10):
		data = serializer.data[i]
		
		imgDir = "static/img/img{}.jpg".format(data["id"])
		if imgDir not in address:
			print("NOT IN A")
			base64_type = data["image"].encode("utf-8")
			decoded_utf = base64.decodebytes(base64_type)
			byteImage = np.frombuffer(decoded_utf, dtype=np.uint8)

			frame = Image.open(io.BytesIO(byteImage))
			frame.save("static/img/img{}.jpg".format(data["id"]))

		person = {"name": data["name"], "id": data["studentid"], "imageid":data["id"], "type":data["type"]}
		ctx.append(person)

	# print("NEW CONTEXT: ", ctx)
	
	new_ctx = []

	start = 0

	index = 0
	# print("DATE: ", date)
	base = 0
	for item in date:
		base += item[1]
		
		# new_ctx.append(ctx[start:base])
		new_ctx.append([date[index][0]])
		new_ctx[index].append(date[index][1])

		new_ctx[index].append(ctx[start:base])

		
		start += item[1]
		index += 1

	# context.append(new_ctx)
	# context.append(date)
	# print("Serializer Data\n\n: ", context)


	return render(request, "account/dashboard.html", {"context":new_ctx})

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
	
	"""
	base64_type = img.encode("utf-8")
	decoded_utf = base64.decodebytes(base64_type)
	byteImage = np.frombuffer(decoded_utf, dtype=np.uint8)
	
	frame = Image.open(io.BytesIO(byteImage))
	"""
	
	# frame = cv2.imdecode(byteImage, flags=1)


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