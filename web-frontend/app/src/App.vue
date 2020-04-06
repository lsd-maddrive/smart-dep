<template>
  <div id="app">
    <!-- <b-navbar toggleable="lg" type="dark" variant="info"> -->
    <Slide>
      <a id="home" href="#">
        <span>Home</span>
      </a>
    </Slide>
    <!-- <b-navbar-brand href="#">NavBar</b-navbar-brand>
    </b-navbar>-->
    <main id="page-wrap">
      <router-view />
    </main>
  </div>
</template>

<script>
import { Slide } from "vue-burger-menu";

export default {
  name: "App",
  components: {
    Slide
  }
};
</script>

<style>
html {
  height: 100%;
  overflow: hidden;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
