<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar color="primary" dark flat>
                <v-toolbar-title>Вход</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form ref="form">
                  <v-text-field
                    label="Логин"
                    v-model.trim="username"
                    :rules="nameRules"
                    name="login"
                    prepend-icon="mdi-account"
                    type="text"
                    required
                  ></v-text-field>

                  <v-text-field
                    id="password"
                    label="Пароль"
                    name="password"
                    v-model="password"
                    :rules="[v => !!v || 'Пароль обязателен!']"
                    prepend-icon="mdi-lock"
                    type="password"
                    required
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="handleSubmit" :loading="loading">Вход</v-btn>
                <v-btn color="primary" :to="{name: 'Register'}" :disabled="loading">Регистрация</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      nameRules: [
        v => !!v || 'Логин обязателен!',
        // v => (v && v.length <= 10) || 'Name must be less than 10 characters',
      ],
      password: "",
      loading: false,

      // emailRules: [
      //   v => !!v || 'E-mail is required',
      //   v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      // ],
    };
  },
  computed: {
  },
  methods: {
    handleSubmit: function() {
      let validationResult = this.$refs.form.validate()
      if (!validationResult) {
        return
      }

      this.loading = true;
      const { username, password } = this;
      if (username && password) {
        this.$store.dispatch("auth/login", { username, password }).then(
          () => {
            this.$toasted.success("Успешный вход!");
            this.$router.push(this.$route.query.returnUrl || { name: "Home" });
          },
          error => {
            this.$toasted.error("Вход не удался: " + error);
            this.loading = false;
          }
        );
      }
    }
  }
};
</script>

<style scoped>
</style>

