from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from education.models import Course
from permissions.models import Permission
from .models import UserProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer, StudentsSerializer, UpdateProfileSerializer

class UserProfileListCreateView(ListCreateAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly, permissions.IsAuthenticated]

class UpdateUserProfileView(APIView):

    @staticmethod
    def put(request, userId=None):
        try:
            user = request.user

            if not Permission.CanUpdateUserProfileSpecificUsers(user=user, targetUserId=userId):
                return Permission.GetNoPermissionResponse()

            userProfile = UserProfile.objects.get(user=userId)

            updateData = {
                'firstName': request.data['firstName'],
                'lastName': request.data['lastName'],
                'city': request.data['city'],
                'phone': request.data['phone']
            }

            updatedprofile = UpdateProfileSerializer(instance=userProfile, data=updateData)

            if not updatedprofile.is_valid():
                return Response(
                    data=updatedprofile.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            updatedprofile.save()

            return Response(data=updatedprofile.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudentsView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    @staticmethod
    def get(request, courseId=None):
        '''Вывод учеников курса'''

        try:

            user = request.user

            if not Permission.CanReadUserProfileAnyUsersSpecificCourses(user=user,
                                                                        targetCourseId=courseId):
                return Permission.GetNoPermissionResponse()

            course = Course.objects.get(pk=courseId)
            students = StudentsSerializer(course)

            return Response(students.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
