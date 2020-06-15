<template>
  <v-btn block :outlined="!enabled" :loading="loading" color="primary" @click="enabled=!enabled">
    <span>'{{ name }}' {{ enabled ? 'включен' : 'выключен' }}</span>
    <v-icon class="pl-2">{{icon}}</v-icon>
    <v-icon v-if="isDeviceLost" class="pl-2">mdi-alert</v-icon>
  </v-btn>
</template>

<script>
export default {
  props: {
    id: String
  },
  data() {
    return {
      loading: false
    };
  },
  computed: {
    isDeviceLost() {
      const deviceState = this.$store.getters[`getDeviceById`](this.id);
      if (deviceState) {
        var diff_ms = Date.now() - (deviceState.last_ts * 1000) - deviceState.fb_diff_ms;
        return diff_ms > 5000;
      }

      return false;
    },
    name() {
      const deviceState = this.$store.getters[`getDeviceById`](this.id);
      return deviceState ? deviceState.name : "";
    },
    icon() {
      const deviceState = this.$store.getters[`getDeviceById`](this.id);
      return deviceState ? deviceState.icon_name : "";
    },
    enabled: {
      get() {
        const deviceState = this.$store.getters[`getDeviceById`](this.id);
        return deviceState ? deviceState.state.enabled : false;
      },
      set(value) {
        this.loading = true;
        this.$store
          .dispatch("commandState", { id: this.id, enabled: value })
          .then(resp => {
            this.$toasted.success("Команда отправлена, подождите обновления");
            this.loading = false;
          })
          .catch(err => {
            this.$toasted.error("Не удалось отправить команду");
            this.loading = false;
          });
      }
    }
  },
  methods: {},
  mounted() {}
};
</script>

<style>
</style>
