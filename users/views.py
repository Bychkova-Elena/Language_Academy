<<<<<<< HEAD
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer
=======

# class GetUserProfileView(APIView):
#     def get(self, request, format=None):
#         try:
#             user = self.request.user
#             username = user.username

#             user_profile = UserProfile.objects.get(user=user)
#             user_profile = UserSerializer(user_profile)

#             return Response({ 'profile': user_profile.data, 'username': str(username) })
#         except:
#             return Response({ 'error': 'Something went wrong when retrieving profile' })

# class UpdateUserProfileView(APIView):
#     def put(self, request, format=None):
#         try:
#             user = self.request.user
#             username = user.username

#             data = self.request.data
#             firstName = data['firstName']
#             lastName = data['lastName']
#             phone = data['phone']
#             city = data['city']

#             UserProfile.objects.filter(user=user).update(firstName=firstName, lastName=lastName, phone=phone, city=city)

#             user_profile = UserProfile.objects.get(user=user)
#             user_profile = UserSerializer(user_profile)

#             return Response({ 'profile': user_profile.data, 'username': str(username) })
#         except:
#             return Response({ 'error': 'Something went wrong when updating profile' })
        
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from .models import UserProfile, Teacher
from rest_framework import permissions
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import userProfileSerializer, LanguageTeachersSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
<<<<<<< HEAD
>>>>>>> Group: updating and deleting teachers groups
=======
from rest_framework import status
>>>>>>> Group:  status was added


class UserProfileListCreateView(ListCreateAPIView):
    queryset=UserProfile.objects.all()
<<<<<<< HEAD
    serializer_class=UserProfileSerializer
    permission_classes=[IsAuthenticated]
=======
    serializer_class=userProfileSerializer
    permission_classes=[permissions.IsAuthenticated]
>>>>>>> Group: updating and deleting teachers groups

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)

class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=UserProfile.objects.all()
<<<<<<< HEAD
    serializer_class=UserProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]
=======
    serializer_class=userProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,permissions.IsAuthenticated]
    
class LanguageTeachersView(APIView):
    permission_classes=[permissions.AllowAny] 
    
    def get(self, request, format=None):
        '''Вывод преподаваемых языков'''
    
        try:
            
            user = self.request.user
            
            language = Teacher.objects.filter(user=user)
             
               
            language = LanguageTeachersSerializer(language, many=True)

            return Response({ 'Language': language.data}, status=status.HTTP_200_OK)
            
<<<<<<< HEAD
        except:
          return Response({ 'error': 'Something went wrong when retrieving languages' })
>>>>>>> Group: updating and deleting teachers groups
=======
        except Exception as error:
            return Response({ 'error': str(error) }, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> Group:  status was added
