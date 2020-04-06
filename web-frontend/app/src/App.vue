<template>
  <div id="app">
    <Navbar>
      <MenuButton />
    </Navbar>

    <Sidebar>
      <ul class="sidebar-panel-nav">
        <li v-for="room in this.$store.state.rooms" :key="room.id">
          <a href="#home">Комната {{ room.name }}</a>
        </li>
      </ul>
    </Sidebar>
    <router-view />
  </div>
</template>

<script>
import Navbar from "@/components/Menu/Navbar.vue";
import Sidebar from "@/components/Menu/Side.vue";
import MenuButton from "@/components/Menu/Button.vue";

export default {
  name: "App",
  components: {
    Navbar,
    MenuButton,
    Sidebar
  },
  beforeMount() {
    this.$store.dispatch('syncRooms')
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
