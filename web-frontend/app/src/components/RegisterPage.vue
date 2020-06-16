<template>
  <v-main>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>Регистрация</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form">
                <v-text-field
                  label="Логин"
                  v-model.trim="user.username"
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
                  v-model="user.password"
                  :rules="[v => !!v || 'Пароль обязателен!']"
                  prepend-icon="mdi-lock"
                  type="password"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="handleSubmit" :loading="loading">Зарегистрироваться</v-btn>
              <v-btn color="primary" :to="{name: 'Login'}" :disabled="loading">Отмена</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  data() {
    return {
      user: {
        username: "",
        password: ""
      },
      nameRules: [
        v => !!v || "Логин обязателен!"
        // v => (v && v.length <= 10) || 'Name must be less than 10 characters',
      ],
      loading: false
    };
  },
  computed: {},
  methods: {
    handleSubmit: function() {
      let validationResult = this.$refs.form.validate();
      if (!validationResult) {
        return;
      }

      this.loading = true;
      this.$store.dispatch("auth/register", this.user).then(
        () => {
          this.$toasted.success("Успешная регистрация!");
          this.$router.push({ name: "Home" });
        },
        err => {
          this.$toasted.error("Ошибка регистрации");
          this.loading = false;
        }
      );
    }
  }
};
</script>

<style scoped>
</style>

