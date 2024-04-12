from rest_framework import serializers
from .models import User
import random
from firebase_admin import firestore



class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'username', 'password', 'otp']

		extra_kwargs = { 
		"password": {'write_only':True},
		'otp': {'required': True, 'read_only':True},
		'email': {'required': True},
         'username': {'required': True}
		}

	def validate(self, data):
		email = data.get('email')
		if email:
			db = firestore.client()
			email_query = db.collection('users').where('email', '==', email).limit(1).get()
			if email_query:
				raise serializers.ValidationError('Email already exists')
		return data
