<template>
  <b-container>
    <b-row>
      <b-col md="4">
        <lights-panel></lights-panel>
      </b-col>
      <b-col md="4">
        <power-panel></power-panel>
      </b-col>
      <b-col md="4">
        <env-state-panel></env-state-panel>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import LightsPanel from "@/components/LightsPanel";
import PowerPanel from "@/components/PowerPanel";
import EnvStatePanel from "@/components/EnvStatePanel";

export default {
  name: "RoomControl",
  data() {
    return {};
  },
  computed: {},
  components: {
    "lights-panel": LightsPanel,
    "power-panel": PowerPanel,
    "env-state-panel": EnvStatePanel
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
