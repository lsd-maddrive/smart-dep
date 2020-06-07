<template>
  <v-app>
    <v-app-bar app hide-on-scroll color="primary" dark>
      <v-app-bar-nav-icon @click.stop="sidebarMenu = !sidebarMenu"></v-app-bar-nav-icon>
      <v-toolbar-title>
        <router-link :to="{name: 'Home'}" tag="span" style="cursor: pointer">Умная кафедра</router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <!-- <v-icon>mdi-account</v-icon> -->

      <v-btn v-if="!isLoggedIn" color="primary" :to="{ name: 'Login' }">
        <!-- <v-btn value="feed"> -->
        <span>Вход</span>
        <!-- <v-icon>???</v-icon> -->
        <!-- </v-btn> -->
      </v-btn>
      <!-- <router-link v-if="isLoggedIn" :to="{ name: 'Login' }" tag="v-btn"> -->

      <v-tooltip v-if="isLoggedIn" bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon :to="{name: 'Home'}" v-on="on">
            <v-icon>mdi-home</v-icon>
          </v-btn>
        </template>
        <span>Домой</span>
      </v-tooltip>

      <v-tooltip v-if="socketsConnected" bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-link</v-icon>
          </v-btn>
        </template>
        <span>Сервер подключен</span>
      </v-tooltip>
      <v-tooltip v-else bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-link-off</v-icon>
          </v-btn>
        </template>
        <span>Сервер отключен</span>
      </v-tooltip>

      <v-tooltip v-if="isLoggedIn" bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon @click="logout" v-on="on">
            <v-icon>mdi-exit-run</v-icon>
          </v-btn>
        </template>
        <span>Выход</span>
      </v-tooltip>

      <v-menu left class="hidden-md-and-up">
        <!-- <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="n in 5" :key="n" @click="() => {}">
            <v-list-item-title>Option {{ n }}</v-list-item-title>
          </v-list-item>
        </v-list> -->
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer v-model="sidebarMenu" floating app color="primary" dark></v-navigation-drawer>
    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>

    <v-footer app></v-footer>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  components: {
  },
  data() {
    return {
      sidebarMenu: false,
    };
  },
  computed: {
    socketsConnected() {
      return this.$store.state.isConnected
    },
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
    axios.interceptors.response.use(undefined, err => {
      return new Promise(function(resolve, reject) {
        if (
          [401, 403].indexOf(err.status) !== -1 &&
          err.config &&
          !err.config.__isRetryRequest
        ) {
          this.$store.dispatch("auth/logout");
          location.reload(true);
        }
        throw err;
      });
    });
  },
  mounted() {}
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
