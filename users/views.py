from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from .models import UserProfile
from rest_framework import permissions
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import userProfileSerializer

class UserProfileListCreateView(ListCreateAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=userProfileSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=userProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,permissions.IsAuthenticated]
    

