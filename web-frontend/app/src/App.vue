<template>
  <v-app>
    <v-navigation-drawer
      v-model="sidebarMenu"
      floating
      app
      color="primary"
      dark
      :clipped="$vuetify.breakpoint.lgAndUp"
    >
      <v-list dense>
        <!-- <template > -->
        <!-- <v-row v-if="item.heading" :key="item.heading" align="center">
            <v-col cols="6">
              <v-subheader v-if="item.heading">{{ item.heading }}</v-subheader>
            </v-col>
            <v-col cols="6" class="text-center">
              <a href="#!" class="body-2 black--text">EDIT</a>
            </v-col>
          </v-row>
          <v-list-group
            v-else-if="item.children"
            :key="item.text"
            v-model="item.model"
            :prepend-icon="item.model ? item.icon : item['icon-alt']"
            append-icon
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>{{ item.text }}</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item v-for="(child, i) in item.children" :key="i" link>
              <v-list-item-action v-if="child.icon">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>{{ child.text }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
        </v-list-group>-->

        <!-- <v-list-item-group v-model="group" active-class="text--accent-4"> -->
        <v-list-item v-for="item in navItems" :key="item.text" link :to="{name: item.to}">
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- </v-list-item-group> -->

        <!-- </template> -->
      </v-list>

      <!--
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">Меню</v-list-item-title>
          <v-list-item-subtitle>Меню</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-devices</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>
              <router-link :to="{name: 'RegDevices'}" tag="span" style="cursor: pointer">Установка устройств</router-link>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>-->
    </v-navigation-drawer>

    <v-app-bar app hide-on-scroll color="primary" dark :clipped-left="$vuetify.breakpoint.lgAndUp">
      <v-app-bar-nav-icon v-if="isLoggedIn" @click.stop="sidebarMenu = !sidebarMenu"></v-app-bar-nav-icon>
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

      <v-tooltip v-if="isLoggedIn && socketsConnected" bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon >
            <v-icon v-on="on">mdi-link</v-icon>
          </v-btn>
        </template>
        <span>Сервер подключен</span>
      </v-tooltip>
      <v-tooltip v-if="isLoggedIn && !socketsConnected" bottom>
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

      <!-- <v-menu left class="hidden-md-and-up">
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="n in 5" :key="n" @click="() => {}">
            <v-list-item-title>Option {{ n }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>-->
    </v-app-bar>

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
import { mapState } from "vuex";

export default {
  name: "App",
  components: {},
  data() {
    return {
      sidebarMenu: null,
      navItems: [
        { icon: "mdi-home", text: "Домой", to: "Home" },
        { icon: "mdi-devices", text: "Новые устройства", to: "RegDevices" }
      ]
    };
  },
  computed: {
    socketsConnected() {
      return this.$store.state.isConnected;
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
</style>
