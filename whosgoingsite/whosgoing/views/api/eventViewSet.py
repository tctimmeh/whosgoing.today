from rest_framework.viewsets import ModelViewSet
from whosgoing.serializers.event import EventSerializer


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        return self.request.user.events.order_by('name')

    def perform_create(self, serializer):
        event = serializer.save()
        event.add_member(self.request.user)
        return event
