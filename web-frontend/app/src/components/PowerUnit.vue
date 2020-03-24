<template>
    <div class="main">
      <b-button block :pressed="!this.on" variant="outline-dark" @click="pressed()" >
        <div class="data">
          <span>
            Модуль {{ this.on ? 'включен' : 'выключен' }}
          </span>
          <ion-icon name="flash-outline"></ion-icon>
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

.power_button ion-icon {
  float: right;
  font-size: 24px;
}

</style>
