from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from whosgoing.models import EventOccurrence
from whosgoing.serializers.occurrenceMember import OccurrenceMemberSerializer


class EventOccurrenceSerializer(HyperlinkedModelSerializer):
    members = OccurrenceMemberSerializer(source='occurrencemember_set', many=True)
    class Meta:
        model = EventOccurrence
        fields = ('time', 'members')

        extra_kwargs = {
            'members': {'view_name': 'whosgoing:api:occurrencemember-detail'}
        }
