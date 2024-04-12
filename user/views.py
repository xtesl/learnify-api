from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import send_mail
from firebase_admin import firestore

db_client = firestore.client()

from .serializers import UserSerializer
from .models import User
import random

class CreateUser(APIView):
	permission_classes = [AllowAny]
	authentication_classes = []
	
	def post(self, request, *args, **kwargs):
		userSerializer = UserSerializer(data=request.data)
		
		if userSerializer.is_valid():
			doc_ref = db_client.collection('users').document()
			data = userSerializer.validated_data
			data['activated'] = False
			otp = str(random.randint(10000, 999999))
			data['otp'] = otp
			doc_ref.set(data)
			userSerializer.save()

			user_email = request.data.get('email')
			subject = 'Confirmation Code'
			message = f"User's code is: {otp}, please follow this link to confirm user i.e {user_email}: https://learnify-confirm-page.onrender.com"
			from_ = 'Vyndly <noreply@example.com>'
			recipient_list = ["r00399544@gmail.com"]
			send_mail(
                subject=subject,
                message=message,
                from_email=from_,
                recipient_list=recipient_list,
                fail_silently=True
            )
			return Response(userSerializer.data)
		else:
			return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class Login(APIView):
	authentication_classes = []
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		email = request.data.get('email')
		password = request.data.get('password')
		user = db_client.collection('users').where('email', '==', email).limit(1).get()

		if user:
			user_data = user[0].to_dict()
			db_password = user_data.get('password')
			activated = user_data.get('activated')
			if password == db_password and activated:
				return Response(status=status.HTTP_200_OK)
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)



class ConfirmUser(APIView):
	permission_classes = [AllowAny]
	authentication_classes = []


	def post(self, request, *args, **kwargs):
		otp = request.data.get('otp')
		email = request.data.get('email')

		try:
			user = db_client.collection('users').where('email', '==', email).limit(1).get()
			print(user)
			if user:
				db_otp = user[0].to_dict().get('otp')
				if db_otp == otp:
					doc = user[0]
					doc.reference.update({
						'activated': True
					})
					return Response(status=status.HTTP_200_OK)
				else:
					return Response(status=status.HTTP_401_UNAUTHORIZED)
		except Exception as e:
			
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
