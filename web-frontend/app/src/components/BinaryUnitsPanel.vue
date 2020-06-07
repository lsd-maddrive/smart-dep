<template>
  <v-card class="elevation-8">
    <v-card-title class="justify-center">Управление устройствами</v-card-title>
    <v-card-actions>
      <v-row>
        <v-col cols="12" md="6">
          <div class="pb-2 text-center">Управление светом</div>
          <v-row class="ma-1" align="stretch" v-for="unit in light_units" :key="unit.id">
            <unit :id="unit.id" prefix="Свет" type="light" icon="mdi-lightbulb-on"></unit>
          </v-row>
        </v-col>
        <v-col cols="12" md="6">
          <div class="pb-2 text-center">Управление электричеством</div>
          <v-row class="ma-1" align="stretch" v-for="unit in power_units" :key="unit.id">
            <unit :id="unit.id" prefix="Модуль" type="power" icon="mdi-lightning-bolt"></unit>
          </v-row>
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
    light_units() {
      return this.$store.state.light.units;
    },
    power_units() {
      return this.$store.state.power.units;
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
