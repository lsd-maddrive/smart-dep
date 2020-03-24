<template>
  <div class="card" >
    <div class="card-header">Состояние комнаты</div>
    <div class="card-body" >
      <div class="state-data">
        <ion-icon name="thermometer-outline"></ion-icon>
        <span>Температура: {{ state.temp }}</span> 
      </div>
      <div class="state-data">
        <ion-icon name="water-outline"></ion-icon>
        <span>Влажность: {{ state.humid }} %</span> 
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      state: this.$store.state.environ.data
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.state-data {
  padding: 6px 10px;
}

ion-icon {
  float: left;
  font-size: 24px;
}
</style>
