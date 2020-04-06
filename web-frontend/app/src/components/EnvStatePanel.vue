<template>
  <div>
    <b-card no-body>
      <b-card-header>
        <b-button block href="#" v-b-toggle.env-panel-data>Состояние комнаты</b-button>
      </b-card-header>
      <b-collapse id="env-panel-data" visible role="tabpanel">
        <b-card-body class="card-body power-panel">
          <div class="state-data">
            <ion-icon name="thermometer-outline"></ion-icon>
            <span>Температура: {{ envState.temp }}</span>
          </div>
          <div class="state-data">
            <ion-icon name="water-outline"></ion-icon>
            <span>Влажность: {{ envState.humid }} %</span>
          </div>
          <div class="chart">
            <TempChart :styles="myStyles" />
          </div>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import TempChart from "@/components/TempChart.vue";

export default {
  data() {
    return {};
  },
  computed: {
    ...mapState({
      envState: state => state.environ.data
    }),
    myStyles() {
      return {
        height: "50vh",
        position: "relative"
      };
    }
  },
  components: {
    TempChart
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.state-data {
  padding: 3px 5px;
}

ion-icon {
  float: left;
  font-size: 24px;
}
</style>
