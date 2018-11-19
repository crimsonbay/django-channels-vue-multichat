<template>
  <b-container no-body class="fluid p-0 m-0" id="chat-tabs-all">
    <div v-if="error!=''" style="color:#FF0000">{{error}}<br></div>
      <input type="text" class="m-1" placeholder="Enter a channel name..."
             v-on:keyup.enter="addChannelClick" ref="channelInput" id="channeltInput">
      <b-button type="button" class="btn btn-success" v-on:click="addChannelClick"><span aria-hidden="true">Enter</span></b-button>
    <b-nav tabs class="p-0 m-0">
      <div v-for="(chat,i) in chats">
        <b-nav-item v-if="chat.chatname == activeChat" active id="nav-item-">
          {{chat.chatname}}&nbsp;
            <b-button type="button" class="close" aria-label="Close" v-on:click="closeClick(i)">
              <span aria-hidden="true" background="#000" hover="{width: 230px;}">&times;</span>
            </b-button>
        </b-nav-item>
        <!-- <b-nav-item v-else v-on:click.self="messagesRecieve(chat.chatname)"> -->
        <b-nav-item v-else>
          <div v-on:click.self="messagesRecieve(chat.chatname)">
            {{chat.chatname}}&nbsp;
            <b-button type="button" class="close" aria-label="Close" v-on:click="closeClick(i)"><span aria-hidden="true">&times;</span></b-button>
          </div>
        </b-nav-item>
      </div>
    </b-nav>
    <b-card class="border-top-0 border-bottom-0" ref="chat" id="chat">
      <div class="text-left" v-for="mes in messages">
        [{{mes.time}}] <b>{{mes.user.first_name}}:</b> {{mes.text}}
      </div>
    </b-card>
    <div v-if="chatSocket!=null" class="input-group align-bottom p-0 m-0" id="input-area">
      <input type="text" class="form-control" placeholder="Enter a message..."
             aria-label="Recipient's username" aria-describedby="button-addon2"
             v-on:keyup.enter="postMessage" ref="textInput" id="textInput">
      <div class="input-group-append">
        <button class="btn btn-outline-secondary border-bottom-0" type="button" id="button-addon2" v-on:click="postMessage">Send</button>
      </div>
    </div>
  </b-container>
</template>

<script>
import { fetchLeaveChat, fetchGetUserChats, fetchGetMessages, newSocket } from '../api'
export default {
  name: "ChatTabs",
  data() {
    return {
      name: "Chat", // name to write to the repository of the name of the open page
                          //( имя для записи в хранилище имени открытой страницы)
      chats: [], // chat list( список чатов)
      messages: [], // open chat messages list( список сообщений открытого чата)
      activeChat: '', // open chat name( имя открытого чата)
      chatSocket: null, // open chat socket for sending and receiving messages
                        // ( сокет открытого чата для отправки и получения сообщения)
      error: '', // error message( сообщение об ошибке)
    }
  },
  computed: {
    // user token from store( токен пользователя из store)
    tokenStore() {
      return this.$store.getters.TOKEN;
    },
    // user first_name from store( first_name пользователя из store)
    firstNameStore() {
      return this.$store.getters.FIRST_NAME;
    },

  },
  // after creation( после создания)
  created: function () {
    // меняем имя открытой страницы в хранилище
    this.$store.dispatch('setPageName', {pageName: this.name});
    // request open user chats( запрашиваем открыте чаты пользователя)
    this.getСhats();

    },
  // when updating, scroll the chat page down( при обновлении скроллим страницу чата вниз)
  updated () {
    this.$refs.chat.scrollTop = this.$refs.chat.scrollHeight;
  },
  methods: {
    // check by name if there is already a chat in the chat list( проверяем по имени, есть ли уже чат в списке чатов)
    chatInChats: function (chatName) {
      let repeat = false;
      for (var i in this.chats) {
        if (this.chats[i].chatname == chatName) {
          return true
        }
      };
      return false
    },

    // channel name validation( валидация имени чата)
    channelNameValidation: function (channelName) {
      let pattern = /^[a-z0-9]+$/i
      if (!pattern.test(channelName)) {
        this.$refs.channelInput.value = ''
        this.error = 'В названии канала возможны только латинские буквы и цифры!'
        return false
      } else {
        return true
      }
    },

    // click Enter button (or enter) to add / enter the channel
    // ( нажата кнопка( или enter) добавления/вхождения на канал)
    addChannelClick: function () {
      let channelName = this.$refs.channelInput.value;
      if (!this.channelNameValidation(channelName)) {
        return
      }
      this.$refs.channelInput.value = ''
      if (channelName) {
        this.createSocket(channelName)
        this.activeChat = channelName
        if (!this.chatInChats(channelName)) {
          let chat = {};
          chat.chatname = channelName
          this.chats.push(chat)
        }
      }
    },

    // channel close button pressed( нажата кнопка закрытия канала)
    closeClick: function (i) {
      // if not Anonymous, remove the user from the members of the chat on the backend
      // (если не Аноним, удаляем пользователя из members чата на бэке)
      if (this.firstNameStore != 'Anonymous') {
        this.deleteChat(this.chats[i].chatname);
      };
      if (this.chats[i].chatname === this.activeChat) {
        if (i == (this.chats.length-1)) {
          if (i>0) {
            this.activeChat = this.chats[i-1].chatname;
            this.chats.splice(i,1);
          }
          else {
            this.activeChat = '';
            this.chats = [];
            return 0
          }
        }
        else {
          this.activeChat = this.chats[i+1].chatname;
          this.chats.splice(i,1);
        }
        this.messagesRecieve(this.activeChat);
      }
      else {
        this.chats.splice(i,1);
      }
      return 0
    },

    // remove user from members of chat( удалить пользователя из members чата)
    deleteChat: function(chatName) {
      fetchLeaveChat(chatName)
    },

    // send message via socket( отправить сообщение через сокет)
    postMessage: function () {
      let textMessage = this.$refs.textInput.value;
      this.chatSocket.send(JSON.stringify({
        'message': textMessage,
        'type': 'text',
      }));
      this.$refs.textInput.value = '';
    },

    // requests open user chats and fills them with chats
    // if in the session repository there was a chat for adding after clicking on ChatList
    // we add it too, the last one is made active
    // call createSocket in case of a non-empty set of chats to create a socket of the active chat
    // it will already load the chat history
    // ( запрашвает открытые чаты пользователей и заполняет ими chats
    // если в хранилище сессии был чат для добавления после клика в ChatList
    // то добавляем его тоже, последний делаем активным
    // вызываем createSocket в случае непустого набора chats для создания сокета активного чата
    // в ней уже произойдет подгрузка истории чата)
    getСhats: function () {
      let that = this;
      fetchGetUserChats()
        .then(function(obj){
          //that.activeChat = obj.body[obj.body.length -1].chatname;
          if (obj.status == 200){
            that.chats = obj.body;
          }
          else {
            //that.chats = [];
          };
          let addingChatName = sessionStorage.getItem('chatAdd');
          if (addingChatName) {
            sessionStorage.setItem('chatAdd', '');
            if (!that.chatInChats(addingChatName)) {
              let addingChat = {};
              addingChat.chatname = addingChatName;
              that.chats.push(addingChat)
            }
          };
          if (that.chats.length > 0) {
            that.activeChat = that.chats[that.chats.length - 1].chatname;
            that.createSocket(that.activeChat);
          }
          return obj
          }).catch(console.error.bind(console));
    },
    // fills data massages[] in the reverse order
    // if a message from an empty user then renames it Anonymous
    // ( заполняет data'ой massages[] в обратном порядке, если сообщение от пустого пользователя
    // то переименовывает его а Anonymous)
    messagesFill: function (data, chatName) {
      this.messages = data.slice().reverse();
      for (var i in this.messages) {
        if (!this.messages[i].user) {
          this.messages[i].user = {first_name: 'Anonymous'}
        }
      }
      this.activeChat = chatName;
    },

    // get messages by channel name, call messagesFill function filling messages
    // and call the socket-creating function
    // ( получить сообщения по имени канала, вызвать заполняющую сообщениями функцию messagesFill
    // и вызвать создающую сокет функцию)
    messagesRecieve: function (chatName) {
      let that = this
      fetchGetMessages(chatName)
        .then(function(obj){
          that.messagesFill(obj.body, chatName)
          return obj
        }).catch(console.error.bind(console))
    },

    // creates a socket, loads the history after creation using messagesRecieve and describes how to work with the socket
    // ( создает сокет, подгружает историю после создания при помощи messagesRecieve и описывает работу с сокетом)
    createSocket: function (chatName) {
      var that = this;
      if (this.chatSocket != null) {
        this.chatSocket.close();
      }
      ;
      let token = sessionStorage.getItem('token')
      this.chatSocket = newSocket(chatName)
      this.chatSocket.onerror = function (event) {
        that.error = 'Error connecting to the channel! Try a different name.( Ошибка подключения к каналу! Попробуйте другое имя.)'
        let chatLen = that.chats.length;
        that.closeClick(chatLen-1);
      }
      // request the message history of the opened channel( запрашиваем историю сообщений открывшегося канала)
      this.chatSocket.onopen = function () {
        that.messagesRecieve(that.activeChat);
      };
      this.chatSocket.onclose = function (eventclose) {
      }
      this.chatSocket.onmessage = function (msg) {
        var data = JSON.parse(msg.data);
        that.messages.push(data);
      };
    },
  }
}
</script>

<style scoped>
  #chat {
    height: 60vh;
    border: 0px solid #C1C1C1;
    border-radius: 10px;
    overflow-y: scroll;
  }
  #textInput {
    border-radius: 0px;
  }
  #button-addon2 {
    height: 100%;
    border-radius: 0px;
    background-color: bisque;
  }
</style>