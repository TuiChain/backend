from django.contrib.auth.models import User, Group
from rest_framework import serializers

# Serializers allow complex data such as querysets and model instances to be converted to native 
# Python datatypes that can then be easily rendered into JSON, XML or other content types. 
# Serializers also provide deserialization, allowing parsed data to be converted back into complex types, 
# after first validating the incoming data.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']