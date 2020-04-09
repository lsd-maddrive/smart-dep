<template>
  <div>
    <b-card no-body>
      <b-card-header>
        <b-button block href="#" v-b-toggle.light-panel-data>Управление светом</b-button>
      </b-card-header>
      <b-collapse id="light-panel-data" visible role="tabpanel">
        <b-card-body class="card-body power-panel">
          <light-unit v-for="unit in units" :key="unit.id" :id="unit.id"></light-unit>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>
import LightUnit from "@/components/LightUnit";
import Services from "@/services/Services";

export default {
  data() {
    return {
    };
  },
  computed: {
    units() {
      return this.$store.state.light.units
    }
  },
  components: {
    "light-unit": LightUnit
  },
  methods: {},
  beforeMount() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.lights-panel {
  flex-direction: column;
  display: flex; /* Make the buttons appear below each other */
}

light-unit {
  padding: 6px 10px;
}
</style>
