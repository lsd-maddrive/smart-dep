<template>
  <div>
    <b-container class="bv-example-row">
      <b-row>
        <b-col md="4">
          <lights-panel v-bind:states="sample_lights"></lights-panel>
        </b-col>
        <b-col md="4">
          <power-panel v-bind:states="sample_power_units"></power-panel>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import LightsPanel from '@/components/LightsPanel'
import PowerPanel from '@/components/PowerPanel'

export default {
  name: 'RoomControl',
  data () {
    return {
      sample_power_units: [
        {
          enabled: true,
          id: 0
        },
        {
          enabled: true,
          id: 1
        }
      ],
      sample_lights: [
        {
          enabled: true,
          id: 0
        },
        {
          enabled: true,
          id: 1
        }
      ]
    }
  },
  computed: {

  },
  components: {
    'lights-panel': LightsPanel,
    'power-panel': PowerPanel
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
