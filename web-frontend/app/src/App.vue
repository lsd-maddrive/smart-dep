<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <!-- <b-container> -->
        <MenuButton />
      <!-- </b-container> -->
    </b-navbar>


    <Sidebar>
      <b-button :to="{path: '/'}" class="my-2 w-100">Главная</b-button>
      <b-dropdown id="dropdown-1" text="Доступные комнаты" class="my-2 w-100">
        <b-dropdown-item v-for="room in this.$store.state.rooms" :key="room.id">
          <b-button  :to="{name: 'RoomControl', params: {id: room.id}}">Комната {{ room.name }} [{{ room.id }}]</b-button>
        </b-dropdown-item>
      </b-dropdown>
    </Sidebar>
    
    
    <router-view />
  </div>
</template>

<script>
import Sidebar from "@/components/Menu/Side.vue";
import MenuButton from "@/components/Menu/Button.vue";

export default {
  name: "App",
  components: {
    MenuButton,
    Sidebar
  },
  computed: {
    rooms() {
      return this.$store.state.rooms;
    }
  },
  beforeMount() {
    this.$store.dispatch("syncRooms");
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
