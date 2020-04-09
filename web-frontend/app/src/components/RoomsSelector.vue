<template>
  <div>
    <h3>Привет! Это интерфейс умной кафедры!</h3>
    <!-- <h4 v-if="isProd">Production</h4> -->
    <!-- <h4 v-else>Not Production</h4> -->
    <h4>Вот доступные места:</h4>
    <b-container>
      <div>
        <b-card-group deck>
        <b-card
          title="Помещение"
          tag="article"
          style="max-width: 20rem;"
          class="mb-2"
          v-for="place in this.$store.state.places"
          :key="place.id"
        >
          <b-card-text>Комната {{ place.name }} [{{ place.id.substring(0,5) }}]</b-card-text>
          <b-button :to="{name: 'RoomControl', params: {id: place.id}}" variant="dark">Пройдем-с</b-button>
        </b-card>
        <!--
        <b-button-group size="lg" class="my-2 w-75" vertical>
          <b-button
            class="my-2 w-100"
            v-for="room in this.$store.state.rooms"
            :key="room.id"
            :to="{name: 'RoomControl', params: {id: room.id}}"
          >Комната {{ room.name }}</b-button>
        </b-button-group>-->
      </b-card-group>
      </div>
    </b-container>
  </div>
</template>

<script>
import Services from "@/services/Services";

export default {
  name: "RoomsSelector",
  data() {
    return {
      // isProd: process.env.NODE_ENV == 'production'
    };
  },
  computed: {
    places() {
      return this.$store.state.places;
    }
  },
  methods: {},
  components: {},
  beforeMount() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 h4 {
  text-align: center;
  padding: 10px;
}
</style>
