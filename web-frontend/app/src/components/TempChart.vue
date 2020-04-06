
<script>
import { Line } from "vue-chartjs";

export default {
  extends: Line,
  data: () => ({
    options: {
      responsive: true,
      maintainAspectRatio: false,
      aspectRatio: 2
    }
  }),
  mounted() {
    // Overwriting base render method with actual data.
    this.renderChart(
      {
        labels: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"
        ],
        datasets: [
          {
            label: "Sample data",
            backgroundColor: "#f87979",
            data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
          }
        ]
      },
      this.options
    );
  }
};
</script>
