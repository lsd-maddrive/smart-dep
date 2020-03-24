<template>
  <div class="main">
    <b-button block :pressed="!enabled" variant="outline-dark" @click="enabled=!enabled">
      <div class="data">
        <span>Свет '{{ id }}' {{ enabled ? 'включен' : 'выключен' }}</span>
        <ion-icon name="bulb-outline"></ion-icon>
      </div>
    </b-button>
  </div>
</template>

<script>
export default {
  props: {
    id: String
  },
  data() {
    return {};
  },
  computed: {
    enabled: {
      get() {
        return this.$store.getters["light/enabled"](this.id);
      },
      set(value) {
        this.$store.dispatch("light/setState", { id: this.id, state: value });
      }
    }
  },
  methods: {},
  mounted() {
  }
};
</script>

<style>
.data {
  vertical-align: center;
}

.main {
  padding: 1px 0px;
}

ion-icon {
  float: right;
  font-size: 24px;
}
</style>
