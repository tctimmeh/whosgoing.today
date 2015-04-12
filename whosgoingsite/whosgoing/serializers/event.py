from rest_framework.serializers import HyperlinkedModelSerializer
from whosgoing.models import Event
from whosgoing.serializers.eventOccurrence import EventOccurrenceSerializer


class EventSerializer(HyperlinkedModelSerializer):
    occurrence = EventOccurrenceSerializer(read_only=True, source='next_occurrence')

    class Meta:
        model = Event
        fields = ('url', 'id', 'name', 'description', 'time', 'members', 'occurrence')
        extra_kwargs = {
            'url': {'view_name': 'whosgoing:api:event-detail'},
            'members': {'view_name': 'whosgoing:api:user-detail'},
        }

