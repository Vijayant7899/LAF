from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message

#User Serializer
class UserSerializer(serializers.ModelSerializer):
	password =  serializers.CharField(write_only=True)
	online = serializers.ReadOnlyField(source='userprofile.online')
	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'online']

#Message Serializer

class MessageSerializer(serializers.ModelSerializer):
	sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
	receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
	class Meta:
		model = Message
		fields = ['sender', 'receiver', 'message', 'timestamp']
