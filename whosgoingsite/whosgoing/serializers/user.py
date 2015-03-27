from django.contrib.auth.models import User
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer


class UserSerializer(HyperlinkedModelSerializer):
    events = HyperlinkedRelatedField(many=True, view_name='whosgoing:api:event-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'events')
        extra_kwargs = {
            'url': {'view_name': 'whosgoing:api:user-detail'}
        }
