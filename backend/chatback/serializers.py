from rest_framework import serializers
from .models import User, Message, Chat


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


# serializer to output the user as the first_name field for use in the MessageOutSerializer
# ( serializer для вывода пользователя как поле first_name для использования в MessageOutSerializer)
class UserForMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name',)


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'chatname', 'private', 'members')


# serializer Chat to send out( serializer Chat для отсылки вовне)
class ChatOutSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Chat
        fields = ('id', 'chatname', 'private', 'members')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'user', 'chat', 'time', 'text', 'viewed')


# serializer Message to send out( serializer Message для отсылки вовне)
class MessageOutSerializer(serializers.ModelSerializer):
    user = UserForMessageSerializer()
    time = serializers.DateTimeField(format='%H:%M:%S')

    class Meta:
        model = Message
        fields = ('id', 'user', 'chat', 'time', 'text', 'viewed')
