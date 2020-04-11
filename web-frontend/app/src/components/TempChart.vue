
<script>
import { Line, mixins } from "vue-chartjs";

const { reactiveProp } = mixins;

export default {
  extends: Line,
  mixins: [reactiveProp],
  data: () => ({
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        yAxes: [
          {
            id: "1",
            display: true,
            type: "linear",
            position: "left"
          },
          {
            id: "2",
            display: true,
            type: "linear",
            position: "right",
          }
        ],
        xAxes: [
          {
            gridLines: {
              display: true
            },
            // Тип декартовой оси: временная шкала.
            type: "time",
            time: {
              unit: "second",
              unitStepSize: 5,
              round: "second",
              tooltipFormat: "h:mm:ss a",
              displayFormats: {
                hour: "MMM D, h:mm A"
              }
            },
            display: true
            // Параметры временной шкалы.
            // time: {
            // Формат отображения временной шкалы:
            // displayFormats: {
            // почасовая: 'День/Месяц часы:минуты'.
            // hour: "D/MM HH:mm"
            // },
            // unit: "hour",
            // Шаг сетки: каждые шесть часов.
            // stepSize: 6,
            // Задаем формат даты для парсинга из русской локали.
            // parser: value => moment(value, "DD MMMM HH:mm")
            // }
          }
        ]
      }
    }
  }),
  mounted() {
    this.renderChart(this.chartData, this.options);
  }
};
</script>
