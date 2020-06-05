<template>
  <div>
    <form class="login" @submit.prevent="login">
      <h1>Вход</h1>
      <label>Имя пользователя</label>
      <input required v-model="username" type="text" placeholder="Snoopy" />
      <label>Пароль</label>
      <input required v-model="password" type="password" placeholder="Password" />
      <hr />
      <button type="submit">Вход</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login: function() {
      const { username, password } = this;
      this.$store.dispatch("auth/login", { username, password }).then(() => {
        this.$router.push({name: "Home"});
      });
    }
  }
};
</script>

<style scoped>
</style>

