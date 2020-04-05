<template>
  <b-container>
    <b-button-group vertical>
      <b-button
        v-for="room in rooms"
        :key="room.id"
        @click="$router.push({ path: 'room/'+room.id})"
      >{{ room.name }}</b-button>
    </b-button-group>
  </b-container>
</template>

<script>
import Services from "@/services/Services";

export default {
  name: "RoomsSelector",
  data() {
    return {
      rooms: []
    };
  },
  methods: {
    async updateRooms() {
      const response = await Services.getRooms();
      this.rooms = response.data;
    }
  },
  computed: {},
  components: {},
  beforeMount() {
    this.updateRooms();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
