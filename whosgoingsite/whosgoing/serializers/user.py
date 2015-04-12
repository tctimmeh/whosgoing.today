from django.contrib.auth.models import User
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')
        extra_kwargs = {
            'url': {'view_name': 'whosgoing:api:user-detail'}
        }
