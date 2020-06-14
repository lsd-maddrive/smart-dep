<template>
  <v-main>
    <h1>
      Помещение {{ place_name }}
      <v-btn
        class="ml-2"
        icon
        :to="{name: 'EditRoom', params: {id: placeId}, query: {returnUrl: this.$router.currentRoute}}"
      >
        <v-icon>mdi-puzzle-edit</v-icon>
      </v-btn>
    </h1>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <units-panel></units-panel>
        </v-col>
        <v-col cols="12">
          <env-state-panel></env-state-panel>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import BinaryUnitsPanel from "@/components/BinaryUnitsPanel";
import EnvStatePanel from "@/components/EnvStatePanel";

export default {
  name: "RoomControl",
  data() {
    return {
      placeObj: null
    };
  },
  computed: {
    place_name() {
      return this.placeObj ? this.placeObj.name : "";
    },
    placeId() {
      return this.placeObj ? this.placeObj.id : "";
    }
  },
  components: {
    "units-panel": BinaryUnitsPanel,
    "env-state-panel": EnvStatePanel
  },
  methods: {
    _initialization() {
      const placeId = this.$route.params.id;
      this.$store.dispatch("validatePlace", { placeId: placeId }).then(
        resp => {
          console.log("Room " + placeId + " found!");
          this.placeObj = resp;
          this.$store.commit("enterPlace", placeId);

          this.$store.dispatch("syncDeviceStates", { placeId: placeId }).then(
            resp => {},
            err => {
              this.$toasted.error(
                "Не удалось обновить состояние контроллеров =("
              );
            }
          );

          this.$store.dispatch("startSocketLink");
        },
        err => {
          this.$toasted.error("Комната " + placeId + " не найдена =(");
          console.log("Room " + placeId + " not found: " + err);
          this.$router.push({ name: "Home" });
        }
      );
      // After all validated - setup place
    }
  },
  beforeMount() {
    console.log("beforeMount()");
    this._initialization();
  },
  beforeDestroy() {
    // Remove devices
    this.$store.commit("clearDeviceStates");
    this.$store.dispatch("stopSocketLink");
    console.log("beforeDestroy()");
  },
  // We should use this as $route has parameters after creation
  created() {
    console.log("created()");
  },
  // Called when we move from one to another room
  watch: {
    $route(to, from) {
      console.log("Watch $route() called, to: " + to + " / from: " + from);
      this._initialization();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
