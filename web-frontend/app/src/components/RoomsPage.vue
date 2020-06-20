<template>
  <v-container fluid>
    <h1 class="text-center">Привет! Это интерфейс умной кафедры!</h1>
    <v-row align="center">
      <v-col cols="12" sm="6" md="4" v-for="place in places" :key="place.id">
        <v-card class="elevation-12">
          <v-img v-if="place.imageURL" class="white--text align-end" height="200px" :src="place.image">
          </v-img>

          <v-card-title>{{ place.name }} [{{ place.num }}]</v-card-title>

          <v-card-text class="text--primary">
            <v-chip label color="pink" dark v-if="place.attr_projector" class="mb-2">
              <v-icon>mdi-presentation-play</v-icon>
              <span class="ml-2" v-if="iconsTextVisible">Проектор</span>
            </v-chip>

            <v-chip color="orange" label v-if="place.attr_board" class="mb-2">
              <v-icon>mdi-teach</v-icon>
              <span class="ml-2" v-if="iconsTextVisible">Доска</span>
            </v-chip>

            <v-chip label color="primary" dark v-if="place.attr_computers > 0" class="mb-2">
              <v-icon>mdi-laptop</v-icon>
              <span class="ml-2" v-if="iconsTextVisible">{{place.attr_computers}} компьютеров</span>
              <span class="ml-2" v-else>{{place.attr_computers}}</span>
            </v-chip>

            <v-chip label v-if="place.attr_people" class="mb-2">
              <v-icon>mdi-human-handsup</v-icon>
              <span class="ml-2" v-if="iconsTextVisible">{{place.attr_people}} человек</span>
              <span class="ml-2" v-else>{{place.attr_people}}</span>
            </v-chip>
          </v-card-text>
          <v-divider></v-divider>

          <v-card-actions>
            <v-btn text :to="{name: 'RoomControl', params: {id: place.id}}">Управление</v-btn>

            <v-spacer></v-spacer>

            <v-btn class="ml-2" icon :to="{name: 'EditRoom', params: {id: place.id}}">
              <v-icon>mdi-puzzle-edit</v-icon>
            </v-btn>
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
</template>

<script>
import Services from "@/services/Services";

export default {
  name: "RoomsSelector",
  data() {
    return {
      places: []
    };
  },
  computed: {
    iconsTextVisible() {
      return this.$vuetify.breakpoint.mdAndUp;
    }
  },
  methods: {},
  components: {},
  created() {
    this.$store
      .dispatch("syncPlaces")
      .then(resp => {
        this.places = resp;
        console.log(resp)
        this.places.forEach(place => {
          place.image = `${Services.getApiPrefix(place)}/${place.imageURL}`;
        });
      })
      .catch(err => {
        this.$toasted.error("Не удалось обновить комнаты =(");
        console.log(err);
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
