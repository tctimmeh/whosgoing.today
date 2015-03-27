from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from whosgoing.models import Event
from whosgoing.serializers.event import EventSerializer
from whosgoing.serializers.user import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

