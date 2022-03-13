from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserSerializer

class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserSerializer(user_profile)

            return Response({ 'profile': user_profile.data, 'username': str(username) })
        except:
            return Response({ 'error': 'Something went wrong when retrieving profile' })

class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            data = self.request.data
            firstName = data['firstName']
            lastName = data['lastName']
            phone = data['phone']
            city = data['city']

            UserProfile.objects.filter(user=user).update(firstName=firstName, lastName=lastName, phone=phone, city=city)

            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserSerializer(user_profile)

            return Response({ 'profile': user_profile.data, 'username': str(username) })
        except:
            return Response({ 'error': 'Something went wrong when updating profile' })
