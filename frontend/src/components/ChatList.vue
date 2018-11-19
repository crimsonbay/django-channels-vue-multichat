<template>
  <b-container no-body class="fluid p-0 m-0" id="chat-list-all">
    <div class="m-1" v-for="chat in chats" no-body>
      <router-link to="/chat" v-on:click.native="linkClick(chat.chatname)">{{chat.chatname}}</router-link>
    </div>
  </b-container>
</template>

<script>
  import { fetchGetAllChats } from '../api'
  export default {
    name: "ChatList",
    data() {
      return {
        name: 'ChatList', // name to write to the repository of the name of the open page
                          // ( имя для записи в хранилище имени открытой страницы)
        chats: [], // chat list( список чатов)
      }
    },
    // after creation( после создания)
    created: function () {
      // change the name of the open page in the repository( меняем имя открытой страницы в хранилище)
      this.$store.dispatch('setPageName', {pageName: this.name})
      // request a list of non-privileged chats and fill in chats []
      // (запрашиваем список неприватных чатов и заполняем chats[])
      this.getChatList()
    },
    methods: {
      // when clicking on the chat link
      // (при нажатии на ссылку чата)
      linkClick: function (chatName) {
        // add chat to the sessionStorage to add to bookmarks after switching to ChatTabs
        // ( добавляем в хранилище сессии чат для добавлении в закладки после перехода на ChatTabs)
        sessionStorage.setItem('chatAdd', chatName)
      },

      // request a list of non-privileged chats and fill in chats []
      // ( запрашиваем список неприватных чатов и заполняем chats[])
      getChatList: function () {
        let that = this
        fetchGetAllChats()
          .then(function(obj){
            that.chats = obj.body
            return obj.body[obj.body.length -1].chatname
          }).catch(console.error.bind(console))
      }
    }
  }
</script>

<style scoped>

</style>