from django.contrib.auth.models import User
from rest_framework.viewsets import ReadOnlyModelViewSet
from whosgoing.serializers.user import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
