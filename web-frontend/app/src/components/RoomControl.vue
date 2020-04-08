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
    return {};
  },
  computed: {
    place_name() {
      let room = this.$store.state.rooms.find(room => room.id == this.place_id);
      if (room === undefined) {
        return ''
      } else {
        return room.name;
      }
    },
    place_id() {
      return this.$route.params.id;
    }
  },
  components: {
    "lights-panel": LightsPanel,
    "power-panel": PowerPanel,
    "env-state-panel": EnvStatePanel
  },
  beforeMount: function() {
    console.log("beforeMounted()");
    this.$store.dispatch('switchRoom', { place_id: this.place_id });
  },
  beforeDestroy: function() {
    console.log("beforeDestroy()");
  },
  watch: {
    $route(to, from) {
      console.log("Watch $route() called");
      // TODO - reset when updated
      this.$store.dispatch('switchRoom', { place_id: this.place_id });
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
