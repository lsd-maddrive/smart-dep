<template>
  <div class="card" >
    <div class="card-header">Управление электричеством</div>
    <div class="card-body power-panel" >
      <power-unit v-for="unit in units" :key="unit.id" v-bind:enabled="unit.enabled"></power-unit>
    </div>
  </div>
</template>

<script>
import PowerUnit from '@/components/PowerUnit'

export default {
  props: {
    states: Array
  },
  data () {
    return {
      units: this.states
    }
  },
  components: {
    'power-unit': PowerUnit
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.power-panel {
  flex-direction: column;
  display: flex; /* Make the buttons appear below each other */
}
</style>
