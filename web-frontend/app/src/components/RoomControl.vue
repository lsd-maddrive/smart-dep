<template>
  <b-container>
    <b-row>
      <div>
        <span>Комната '{{ place_id }}'</span>
      </div>
    </b-row>
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
  computed: {
    place_id() {
      return this.$route.params.id;
    }
  },
  components: {
    "lights-panel": LightsPanel,
    "power-panel": PowerPanel,
    "env-state-panel": EnvStatePanel
  },
  mounted: function() {
    console.log("mounted()");
    console.log('Send emit on "start_states"');
    this.$socket.emit("start_states", {
      period: 1,
      place_id: this.place_id
    });
  },
  beforeDestroy: function() {
    console.log("beforeDestroy()")
  },
  watch: {
    $route(to, from) {
      console.log("Watch $route() called");
      // TODO - reset when updated
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
