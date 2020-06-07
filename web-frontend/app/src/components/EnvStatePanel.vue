<template>
  <v-card class="elevation-8">
    <v-card-title class="justify-center">Состояние комнаты</v-card-title>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-row justify="center">
            <span>Температура: {{ Math.round(temperature) }}&#176;C</span>
          </v-row>
          <v-row justify="center">
            <span>Влажность: {{ Math.round(humidity) }} %</span>
          </v-row>
          <v-row justify="center">
            <v-col cols="12">
              <TempChart :styles="myStyles" :chart-data="chartData" />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import TempChart from "@/components/TempChart.vue";

export default {
  data() {
    return {
      chartData: {
        datasets: []
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
        height: "40vh",
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
            yAxisID: "1",
            borderColor: "#ff2f2f8f",
            fill: false,
            data: this.temp_vals
          },
          {
            label: "Влажность",
            yAxisID: "2",
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
</style>
