<template>
  <v-card class="elevation-8">
    <v-card-title class="justify-center">Управление устройствами</v-card-title>
    <v-card-actions>
      <v-row class="ma-1" align="stretch">
        <v-col cols="12" sm="6" lg="4" v-for="unit in units" :key="unit.device_id">
          <unit :id="unit.device_id"></unit>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
import BinaryUnit from "@/components/BinaryUnit";
import Services from "@/services/Services";

export default {
  data() {
    return {};
  },
  computed: {
    units() {
      return this.$store.state.deviceStates;
    }
  },
  components: {
    unit: BinaryUnit
  },
  methods: {},
  beforeMount() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
