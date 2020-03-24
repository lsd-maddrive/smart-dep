<template>
  <div class="card">
    <div class="card-header">Управление светом</div>
    <div class="card-body lights-panel">
      <light-unit v-for="unit in units" :key="unit.id" :id="unit.id"></light-unit>
    </div>
  </div>
</template>

<script>
import LightUnit from "@/components/LightUnit";

export default {
  data() {
    return {
      units: this.$store.state.light.units
    };
  },
  components: {
    "light-unit": LightUnit
  }
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
