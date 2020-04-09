<template>
  <div>
    <b-card no-body>
      <b-card-header>
        <b-button block href="#" v-b-toggle.power-panel-data>Управление электричеством</b-button>
      </b-card-header>
      <b-collapse id="power-panel-data" visible role="tabpanel">
        <b-card-body class="card-body power-panel">
          <power-unit v-for="unit in units" :key="unit.id" :id="unit.id"></power-unit>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>
import PowerUnit from "@/components/PowerUnit";

export default {
  data() {
    return {
    };
  },
  computed: {
    units() {
      return this.$store.state.power.units
    }
  },
  components: {
    "power-unit": PowerUnit
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.power-panel {
  flex-direction: column;
  display: flex; /* Make the buttons appear below each other */
}

power-unit {
  padding: 6px 10px;
}
</style>
