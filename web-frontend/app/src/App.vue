<template>
  <div id="app">
    <b-navbar v-if="isLoggedIn" toggleable="lg" type="dark" variant="dark">
      <!-- <b-container> -->
      <MenuButton />
      <!-- </b-container> -->
      <b-button class="my-0" @click="logout">Выход</b-button>
    </b-navbar>

    <Sidebar>
      <b-button :to="{name: 'Home'}" class="my-2 w-100">Главная</b-button>
      <b-dropdown id="dropdown-1" text="Доступные комнаты" class="my-2 w-100">
        <b-dropdown-item v-for="place in places" :key="place.id">
          <b-button
            :to="{name: 'RoomControl', params: {id: place.id}}"
          >Комната {{ place.name }} [{{ place.id.substring(0,5) }}]</b-button>
        </b-dropdown-item>
      </b-dropdown>
    </Sidebar>

    <router-view />
  </div>
</template>

<script>
import Sidebar from "@/components/Menu/Side.vue";
import MenuButton from "@/components/Menu/Button.vue";

import axios from 'axios'

export default {
  name: "App",
  components: {
    MenuButton,
    Sidebar
  },
  data() {
    return {};
  },
  computed: {
    places() {
      return this.$store.state.places || [];
    },
    isLoggedIn() {
      return this.$store.getters["auth/isAuthenticated"];
    }
  },
  methods: {
    logout: function() {
      this.$store.dispatch("auth/logout").then(() => {
        this.$router.push({ name: "Login" });
      });
    }
  },
  created: function() {
    axios.interceptors.response.use(undefined, function(err) {
      return new Promise(function(resolve, reject) {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch("auth/logout");
        }
        throw err;
      });
    });

  },
  mounted() {
    
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
