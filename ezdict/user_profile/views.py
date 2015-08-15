from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models import UserProfile
from serializers import UserProfileSerializer


class UserProfileView(APIView):
    """
    View to control user profile
    """

    def get(self, request):
        profile = UserProfile.findByUser(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
