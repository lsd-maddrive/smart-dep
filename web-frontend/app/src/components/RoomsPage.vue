<template>
  <v-app id="inspire">
    <h1>Привет! Это интерфейс умной кафедры!</h1>
    <h2>Вот доступные места:</h2>
    <v-container fluid>
      <v-row>
        <v-col cols="12" sm="6" md="4" v-for="place in places" :key="place.id">
          <v-card class="elevation-12">
            <v-card-title class="justify-center">
              {{ place.id.substring(0,5) }}
              <v-btn class="ml-2" icon :to="{name: 'EditRoom', params: {id: place.id}}">
                <v-icon>mdi-puzzle-edit</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text class="headline text-center">Комната {{ place.name }}</v-card-text>
            <v-card-actions>
              <v-btn
                block
                color="primary"
                :to="{name: 'RoomControl', params: {id: place.id}}"
              >Пройдемте-с</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <!-- Another card with new room -->
        <v-col cols="12" sm="6" md="4">
          <v-card class="elevation-12">
            <v-card-actions>
              <v-btn block color="primary" :to="{name: 'NewRoom'}">
                <v-icon>mdi-plus</v-icon>Новое помещение
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import Services from "@/services/Services";

export default {
  name: "RoomsSelector",
  data() {
    return {};
  },
  computed: {
    places() {
      return this.$store.state.places || [];
    }
  },
  methods: {},
  components: {},
  created() {
    this.$store
      .dispatch("syncPlaces")
      .then(resp => {})
      .catch(err => {
        this.$toasted.error("Не удалось обновить комнаты =(");
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
