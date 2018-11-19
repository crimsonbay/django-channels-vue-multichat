<template>
  <!-- <div class="text-center" id="home"> Home </div> -->
  <b-container fluid class="p-1 m-1" id="home">
    <div class="p-1 m-1">
      Это простейший сайт чатов. Зарегестрированные пользователи могут создавать комнаты в чатах, общаться же можно и без регистрации.
      Список всех неприватных чатов представлен во вкладке <b>ChatList</b>. На ней можно кликнуть прямо на название комнаты и перейти к общению на вкладку <b>Chat</b>.
    </div>
    <img src="../assets/images/chatlist.png">
    <div>
      У зарегистрированных пользователей список открытых чатов запониминается, и они могу создавать новые комнаты. Незарегистрированные могут входить в комнаты, созданные другими, но список открытых чатов не будет запоминаться при выходе из вкладки <b>Chat</b>.
    </div>
    <img src="../assets/images/chat_user_full.png">
    <div>
      На вкладке <b>Registration</b> можно зарегистрировать пользователя.
    </div>
    <img src="../assets/images/registration.png">
  </b-container>
</template>
<script>
  export default {
    name: "Home",
    data () {
      return{
        name: "Home", // name to write to the repository of the name of the open page
                      // ( имя для записи в хранилище имени открытой страницы)
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
  #home{
    font-size: 130%;
  }
</style>