from rest_framework import viewsets
from ezdict.ezdict_api.serializers import UserSerializer
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model


class CreateUserView(CreateAPIView):
    """
    API endpoint that allows users to be created.
    """
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
