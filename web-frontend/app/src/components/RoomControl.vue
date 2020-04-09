<template>
  <div>
    <div id="main">
      <h3>Комната {{ place_name }}</h3>
    </div>
    <b-container>
      <b-row>
        <b-col md="6">
          <lights-panel class="my-2"></lights-panel>
        </b-col>
        <b-col md="6">
          <power-panel class="my-2"></power-panel>
        </b-col>
        <b-col md="12">
          <env-state-panel class="my-2"></env-state-panel>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import LightsPanel from "@/components/LightsPanel";
import PowerPanel from "@/components/PowerPanel";
import EnvStatePanel from "@/components/EnvStatePanel";

export default {
  name: "RoomControl",
  data() {
    return {
      place_id: this.$route.params.id
    };
  },
  computed: {
    place_name() {
      let place = this.$store.getters.currentPlace
      if (place === undefined) {
        return ''
      } else {
        return place.name;
      }
    },
  },
  components: {
    "lights-panel": LightsPanel,
    "power-panel": PowerPanel,
    "env-state-panel": EnvStatePanel
  },
  beforeMount() {
    console.log("beforeMount()");
    this.$store.dispatch('switchPlace', { place_id: this.place_id });
  },
  beforeDestroy: function() {
    console.log("beforeDestroy()");
  },
  watch: {
    $route(to, from) {
      console.log("Watch $route() called");
      this.$store.dispatch('switchPlace', { place_id: this.place_id });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  text-align: center;
  padding: 10px;
}
</style>
