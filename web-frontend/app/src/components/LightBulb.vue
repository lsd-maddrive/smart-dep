<template>
    <div class="main">
      <b-button block :pressed="!this.on" variant="outline-dark" class="light_button" @click="pressed()" >
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
    }
  }
}
</script>

<style>
.data {
  vertical-align: center;
}

.main {
  padding: 1px 0px;
}

.light_button ion-icon {
  float: right;
  font-size: 24px;
}
</style>
