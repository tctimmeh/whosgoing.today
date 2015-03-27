from rest_framework.fields import CharField
from rest_framework.serializers import HyperlinkedModelSerializer

from whosgoing.models import OccurrenceMember


class OccurrenceMemberSerializer(HyperlinkedModelSerializer):
    attendance = CharField(source='attendance.name', max_length=10)
    class Meta:
        model = OccurrenceMember
        fields = ('user', 'attendance')

        extra_kwargs = {
            'user': {'view_name': 'whosgoing:api:user-detail'}
        }
