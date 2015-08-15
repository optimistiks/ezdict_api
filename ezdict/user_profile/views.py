from rest_framework.response import Response
from rest_framework import status
from models import UserProfile
from serializers import UserProfileSerializer
from rest_framework import generics


class UserProfileView(generics.GenericAPIView):
    """
    View to control user profile
    """

    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        profile = UserProfile.findByUser(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        profile = UserProfile.findByUser(request.user)
        serializer = UserProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
