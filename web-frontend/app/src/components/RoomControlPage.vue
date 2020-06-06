<template>
  <div>
    <div id="main">
      <h3>Комната {{ place_name }}</h3>
    </div>
    <b-container>
      <b-row>
        <b-col md="6">
          <lights-panel class="my-2"></lights-panel>
        </b-col>
        <b-col md="6">
          <power-panel class="my-2"></power-panel>
        </b-col>
        <b-col md="12">
          <env-state-panel class="my-2"></env-state-panel>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import LightsPanel from "@/components/LightsPanel";
import PowerPanel from "@/components/PowerPanel";
import EnvStatePanel from "@/components/EnvStatePanel";

export default {
  name: "RoomControl",
  data() {
    return {
      placeObj: null,
      placeId: null
    };
  },
  computed: {
    place_name() {
      if (this.placeObj === null) {
        return "";
      }
      return this.placeObj.name;
    }
  },
  components: {
    "lights-panel": LightsPanel,
    "power-panel": PowerPanel,
    "env-state-panel": EnvStatePanel
  },
  methods: {
    _initialization() {
      const placeId = this.$route.params.id;
      this.$store.dispatch("validatePlace", { placeId: placeId }).then(
        resp => {
          console.log("Room " + placeId + " found!");
          this.placeObj = resp;
          this.placeId = placeId;

          this.$store.dispatch("light/syncUnits", { placeId: placeId }).then(
            resp => {
              this.$toasted.show("Контроллеры света обновлены");
            },
            err => {
              this.$toasted.show(
                "Не удалось обновить состояние контроллеров света =("
              );
            }
          );

          this.$store.dispatch("power/syncUnits", { placeId: placeId }).then(
            resp => {
              this.$toasted.show("Контроллеры электричества обновлены");
            },
            err => {
              this.$toasted.show(
                "Не удалось обновить состояние контроллеров электричества =("
              );
            }
          );

          this.$store.commit("environ/clearState");
          this.$store.dispatch("startSocketLink", { placeId: placeId });
        },
        err => {
          this.$toasted.show("Комната " + this.placeId + " не найдена =(");
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
h3 {
  text-align: center;
  padding: 10px;
}
</style>
