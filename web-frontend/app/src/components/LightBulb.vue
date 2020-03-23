<template>
    <div class="light_button_main">
      <b-button block :pressed="!this.on" variant="outline-dark" class="light_button" v-on:click="pressed()" >
        <div class="data">
          <span>
            Свет {{ this.on ? 'включен' : 'выключен' }}
          </span>
          <ion-icon name="bulb-outline"></ion-icon>
        </div>
      </b-button>
    </div>
</template>

<script>
export default {
  props: {
    enabled: Boolean
  },
  data () {
    return {
      on: this.enabled
    }
  },
  methods: {
    pressed: function () {
      this.on = !this.on
      console.log('>>>>')
    }
  }
}
</script>

<style>
.data {
  vertical-align: center;
}

.light_button_main {
  padding: 1px 0px;
}

.light_button ion-icon {
  float: right;
  font-size: 24px;
}

.light_button {
  padding: 6px 10px;
}
</style>
