from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.mail import send_mail

from .serializers import UserSerializer
from .models import User

class CreateUser(APIView):
	permission_classes = [AllowAny]
	authentication_classes = []
	
	def post(self, request, *args, **kwargs):
		userSerializer = UserSerializer(data=request.data)

		if userSerializer.is_valid():
			userSerializer.save()

			otp = userSerializer.data.get('otp')
			user_email = request.data.get('email')
			subject = 'Confirmation Code'
			message = f"User's code is: {otp}, please follow this link to confirm user i.e {user_email}: https://learnify-confirm-page.onrender.com"
			from_ = 'Vyndly <noreply@example.com>'
			recipient_list = [user_email]
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
		authenticated_user = authenticate(request, username=email, password=password)

		if authenticated_user and authenticated_user.activated:
			return Response({'message': "Login successful"})
		else:
			return Response({'message':'An error occurred while trying to login, please try again later'},
				status=status.HTTP_401_UNAUTHORIZED)



class ConfirmUser(APIView):
	permission_classes = [AllowAny]
	authentication_classes = []


	def post(self, request, *args, **kwargs):
		otp = request.data.get('otp')
		email = request.data.get('email')

		try:
			user = User.objects.get(email=email)
			
			if user.otp == otp:
				user.activated = True
				user.save()
				return Response({'message': 'User activated'})
			else:
				return Response({'message': 'Wrong otp'}, status=status.HTTP_401_UNAUTHORIZED)
		except User.DoesNotExist:
			return Response({'messag': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
		


