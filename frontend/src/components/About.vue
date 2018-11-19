<template>
  <b-container fluid class="p-1 m-1" id="about">
    <div>
      Это мой учебный проект. Связал воедино Django DRF, Django Channels, Bootstrap и Vue.js. Верстке внимание не уделял.<br>
      В бэкенде <b>3 модели</b>: пользователя, чата и сообщения.<br>
      <b>User</b> - пользователь, содержит username( логин), password( пароль), firstname( Имя).<br>
      <b>Chat</b> - комната чата, содержит ссылку на creator'a( User), chatname, флаг private и members,
      ссылки на участников ManyToManyField(User).<br>
      <b>Message</b> - сообщение, содержит ссылку на отправителя user, ссылку на чат chat, время time,
      текст сообщения text и флаг просмотра viewed.<br>
    </div>
  </b-container>
</template>

<script>
  export default {
    name: "About",
    data () {
      return{
        name: "About", // name to write to the repository of the name of the open page
                       //( имя для записи в хранилище имени открытой страницы)
      }
    },
    // after creation( после создания)
    created: function () {
      // change the name of the open page in the repository( меняем имя открытой страницы в хранилище)
      this.$store.dispatch('setPageName', {pageName: this.name});
    }
  }
</script>

<style scoped>
  #about{
    font-size: 130%;
  }
</style>