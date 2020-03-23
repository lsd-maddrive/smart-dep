<template>
  <div class="card" >
    <div class="card-header">Управление светом</div>
    <div class="card-body lights-panel" >
      <light-bulb v-for="light in lights" :key="light.id" v-bind:enabled="light.enabled"></light-bulb>
    </div>
  </div>
</template>

<script>
import LightBulb from '@/components/LightBulb'

export default {
  props: {
    states: Array
  },
  data () {
    console.log(this.states)
    return {
      lights: this.states
    }
  },
  components: {
    'light-bulb': LightBulb
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.lights-panel {
  flex-direction: column;
  display: flex; /* Make the buttons appear below each other */
}
</style>
