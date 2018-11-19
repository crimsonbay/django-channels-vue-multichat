<template>
  <b-container fluid class="p-0" id="app">
    <div class="row mx-auto m-0">
      <b-nav vertical class=" p-0 " style="width: 13%; height: auto; min-height: 100vh" id="menu">
        <b-nav-item active><router-link to="/">Home</router-link></b-nav-item>
        <b-nav-item><router-link to="/chat-list">ChatList</router-link></b-nav-item>
        <b-nav-item><router-link to="/chat">Chat</router-link></b-nav-item>
        <div v-if="firstNameStore == 'Anonymous'">
          <b-nav-item><router-link to="/registration">Registration</router-link></b-nav-item>
        </div>
        <div v-else>
          <b-nav-item disabled>Registration</b-nav-item>
        </div>
        <b-nav-item><router-link to="/about">About</router-link></b-nav-item>
        </b-nav>
      <div class="col p-0 m-0">
        <div class="col row p-0 m-0" id="cap">
          <div class="col" id="page-name">
            {{namePage}}
          </div>
          <div class="col-3 item text-right">

            <auth-panel></auth-panel>
          </div>
        </div>
        <!-- <chat-tabs class="col m-0 p-0" id="center"></chat-tabs> -->
        <router-view class="col m-0 p-0"></router-view>
      </div>
    </div>
  </b-container>
</template>

<script>
//import ChatTabs from './components/ChatTabs.vue'
import AuthPanel from './components/AuthPanel.vue'


export default {
  name: 'app',
  components: {
    'authPanel': AuthPanel,
  },
  computed: {
    firstNameStore() {
      return this.$store.getters.FIRST_NAME
    },
    namePage() {
      return this.$store.getters.PAGE_NAME
    },
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;

}

#cap {
  background-color: lightseagreen;
  height: 120px;
}

#menu {
  /*justify-content: center;*/
  background-color: #252525;
  height: 100vh;
  border: 1px solid #252525;
}

#page-name {
  font-size: 250%;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
