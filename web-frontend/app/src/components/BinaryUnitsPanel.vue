<template>
  <v-card class="elevation-8">
    <v-card-title class="justify-center">Управление устройствами</v-card-title>
    <v-card-actions>
      <v-row>
        <v-col cols="12" md="12">
          <!-- <div class="pb-2 text-center">Управление устройствами</div> -->
          <v-row class="ma-1" align="stretch" v-for="unit in units" :key="unit.id">
            <unit :id="unit.id"></unit>
          </v-row>
        </v-col>
        <!-- <v-col cols="12" md="12">
          <div class="pb-2 text-center">Управление электричеством</div>
          <v-row class="ma-1" align="stretch" v-for="unit in power_units" :key="unit.id">
            <unit :id="unit.id"></unit>
          </v-row>
        </v-col> -->
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
    },
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
