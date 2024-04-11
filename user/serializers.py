from rest_framework import serializers
from .models import User
import random



class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'username', 'password', 'otp']

		extra_kwargs = { 
		"password": {'write_only':True},
		'otp': {'required': True, 'read_only':True},
		'email': {'required': True},
         'username': {'required': False}
		}

	def create(self, validated_data):
		user = User.objects.create_user(
                validated_data['email'],
                validated_data['username'],
                validated_data['password'],
                otp=str(random.randint(100000, 999999))  
			)
		return user
