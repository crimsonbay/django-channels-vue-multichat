from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework import viewsets
from rest_framework import generics
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, MessageSerializer, MessageOutSerializer, ChatSerializer,\
    ChatOutSerializer
from .models import Message, Chat
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.core import serializers
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.

# returns the first_name of the user if the correct token for the api / check-token request
# (возвращает first_name пользователя в случае правильного токена по запросу api/check-token)
@api_view(['POST'])
def check_token(request):
    return JsonResponse({'firstName': request.user.first_name})


# returns a list of user chats, if authenticated, or [] if not,
# BUT if the all flag is in the request, it returns a list of all non-private chats.
# ( возвращает список чатов пользователя, если аутентифицирован, или [], если нет,
# НО если стоит флаг all в запросе, то возвращает список всех не private чатов)
class ChatListSet(generics.ListAPIView):
    serializer_class = ChatOutSerializer
    def get_queryset(self):
        user = self.request.user
        auth = self.request.auth
        queryset = []
        all = self.request.query_params.get('all', 'false')
        if all == 'true':
            queryset = Chat.objects.filter(private=False)
        elif auth is not None:
            queryset = Chat.objects.filter(members=user)#.order_by('-id')
        return queryset


# returns a list of messages by chat name and number> last_id, if empty, the last_id parameter is looking,
# and then returns all messages> last_id)
# ( возвращает список сообщений по имени чата и номером >last_id, если пусто, смотрит параметр last_id,
# а потом выдает все сообщения >last_id)
class MessageListSet(generics.ListAPIView):
    serializer_class = MessageOutSerializer
    def get_queryset(self):
        #queryset = Messages.objects.all()
        chatname = self.request.query_params.get('chatname', None)
        last_id = self.request.query_params.get('last_id', 0)
        max_count = self.request.query_params.get('max_count', 20)
        if chatname is not None:
            chat = Chat.objects.get(chatname=chatname)
            queryset = Message.objects.filter(
                chat=chat,
                id__gt=last_id
            ).order_by('-id')[:max_count]
        else:
            queryset = Message.objects.filter(
                id__gt=last_id
            ).order_by('-id')[:max_count]
        return queryset


# create a new user at api / add-user by first_name, username and password
# (создать нового пользователя по адресу api/add-user по first_name, username и password)
class NewUserSet(generics.CreateAPIView):
    serializer_class = UserSerializer
    def post(self, request, format=None):
        first_name = self.request.query_params.get('first_name', None)
        username = self.request.query_params.get('username', None)
        password = self.request.query_params.get('password', None)
        data = {}
        try:
            user = User.objects.create_user(username=username, first_name=first_name, password=password)
            stat = status.HTTP_200_OK
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
            stat = status.HTTP_400_BAD_REQUEST
        return Response(data, status=stat)


# leave the chat by user, removes user from chat.members
# (покинуть чат пользователем, удаляет пользователя из members чата)
class LeaveChat(generics.DestroyAPIView):
    serializer_class = ChatSerializer
    def delete(self, request, *args, **kwargs):
        chatname = self.request.query_params.get('chatname', None)
        if (chatname is not None) and (request.user.is_authenticated):
            chat = Chat.objects.get(chatname=chatname)
            chat.members.remove(request.user)
            chat.save()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)