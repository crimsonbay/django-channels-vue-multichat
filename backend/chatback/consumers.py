from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Chat, User
from rest_framework.authtoken.models import Token
from channels.auth import login

import json


class ChatConsumer(AsyncWebsocketConsumer):
    # returns token by key( возвращает token по ключу)
    @database_sync_to_async
    def token_get_key(self, key):
        try:
            token = Token.objects.get(key=key)
        except:
            token = None
        finally:
            return token

    # returns user by id( возвращает user по id)
    @database_sync_to_async
    def user_get(self, id):
        try:
            user = User.objects.get(id=id)
        except:
            user = None
            print('EXCEPT user_get')
        finally:
            return user

    # returns chat by chatname( возвращает chat по chatname)
    @database_sync_to_async
    def chat_get_chatname(self, chatname):
        try:
            chat = Chat.objects.get(chatname=chatname)
        except:
            chat = None
            print('EXCEPT chat_get_chatname')
        finally:
            return chat

    # creates and returns chat by chatname and creator (User), adds to members of creator
    # otherwise returns None
    # (создает и возвращает chat по chatname и creator(User), добавляет в members creator'а
    # иначе возвращает None)
    @database_sync_to_async
    def chat_create(self, chatname, creator):
        try:
            chat = Chat.objects.create(
                chatname=chatname,
                creator=creator,
            )
            chat.members.add(creator)
            chat.save()
        except:
            chat = None
        finally:
            return chat

    # add user to chat members( добавить user в members chat'а)
    @database_sync_to_async
    def chat_add_member(self, user, chat):
        if user is not None:
            chat.members.add(user)
            chat.save()

    # create a message by user, chat and text( создать сообщение по user, chat и text)
    @database_sync_to_async
    def message_create(self, user, chat, text):
        if user is not None:
            return Message.objects.create(
                user=user,
                chat=chat,
                text=text
            )
        else:
            return Message.objects.create(
                chat=chat,
                text=text
            )

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user = self.scope['user']
        # authentication check never passes if the user is not logged in to the admin area
        # but if you are logged in to the admin panel, all the time will be spent as a user who has entered the admin panel,
        # so we remove the check
        # (проверка на аутентификацию не проходит никогда, если пользователь не вошел в админку
        # но если вошел в админку, все время будет проходить в качестве юзера, зашедшего в админку, поэтому
        # проверку убираем)
        # !!! if not user.is_authenticated: !!!
        if True:
            token_key = self.scope['query_string'].decode("utf-8").split('=', 1)[1]
            if token_key!= '':
                token = await self.token_get_key(key=token_key)
                user = await self.user_get(id=token.user_id)
                await login(self.scope, user)
                await database_sync_to_async(self.scope["session"].save)()
            else:
                user = None
        self.room_group_name = 'chat_%s' % self.room_name
        chat = await self.chat_get_chatname(chatname=self.room_name)
        if chat is None:
            if user is None:
                return
            chat = await self.chat_create(
                    chatname=self.room_name,
                    creator=user
                )
        await self.chat_add_member(user, chat)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chatname = self.scope['url_route']['kwargs']['room_name']
        chat = await self.chat_get_chatname(chatname=chatname)
        user = self.scope['user']
        if user.is_authenticated:
            first_name = user.first_name
        else:
            first_name = 'Anonymous'
            user = None
        db_message = await self.message_create(
                user=user,
                chat=chat,
                text=message
            )
        time = str(db_message.time.strftime("%H:%M:%S"))
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': message,
                'user': {'first_name': first_name},
                'time': time
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        text = event['text']
        user = event['user']
        time = event['time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'text': text,
            'user': user,
            'time': time
        }))
