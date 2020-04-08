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
            <span>Температура: {{ Math.round(temperature) }}&#176;C </span>
          </div>
          <div class="state-data">
            <ion-icon name="water-outline"></ion-icon>
            <span>Влажность: {{ Math.round(humidity) }} %</span>
          </div>
          <div class="chart">
            <TempChart :styles="myStyles" :chart-data="chartData" />
          </div>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>
import TempChart from "@/components/TempChart.vue";

import moment from "moment";

export default {
  data() {
    return {
      chartData: {
        datasets: [
        ]
      }
    };
  },
  computed: {
    temperature() {
      this.updateChart();
      return this.$store.getters["environ/tempVal"];
    },
    humidity() {
      return this.$store.getters["environ/humidVal"];
    },
    lightness() {
      return this.$store.getters["environ/lightVal"];
    },

    chart_times() {
      let data = this.$store.getters["environ/times"];
      return data;
    },

    temp_vals() {
      let data = this.$store.getters["environ/temps"];
      return data;
    },

    humid_vals() {
      let data = this.$store.getters["environ/humids"];
      return data;
    },

    myStyles() {
      return {
        height: "50vh",
        position: "relative"
      };
    }
  },
  methods: {
    updateChart() {
      this.chartData = {
        labels: this.chart_times,
        datasets: [
          {
            label: "Температура",
            yAxisID: '1',
            borderColor: "#ff2f2f8f",
            fill: false,
            data: this.temp_vals
          },
          {
            label: "Влажность",
            yAxisID: '2',
            borderColor: "#2f2fff8f",
            fill: false,
            data: this.humid_vals
          }
        ]
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
