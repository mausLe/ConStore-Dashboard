from rest_framework import serializers
from .models import Watchlist

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Watchlist
		fields ='__all__'
        