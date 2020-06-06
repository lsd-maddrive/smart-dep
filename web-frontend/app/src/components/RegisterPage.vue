<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">Имя пользователя</label>
        <input
          type="text"
          v-model="user.username"
          v-validate="'required'"
          name="username"
          class="form-control"
          :class="{ 'is-invalid': submitted && errors.has('username') }"
        />
        <div
          v-if="submitted && errors.has('username')"
          class="invalid-feedback"
        >{{ errors.first('username') }}</div>
      </div>
      <div class="form-group">
        <label for="password">Пароль</label>
        <input
          type="password"
          v-model="user.password"
          v-validate="{ required: true, min: 6 }"
          name="password"
          class="form-control"
          :class="{ 'is-invalid': submitted && errors.has('password') }"
        />
        <div
          v-if="submitted && errors.has('password')"
          class="invalid-feedback"
        >{{ errors.first('password') }}</div>
      </div>
      <div class="form-group">
        <button class="btn btn-primary" :disabled="status.registering">Зарегистрироваться</button>
        <img
          v-show="status.registering"
          src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA=="
        />
        <router-link to="/login" class="btn btn-link">Отмена</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      user: {
        username: "",
        password: ""
      },
      submitted: false
    };
  },
  computed: {
    ...mapState("auth", ["status"])
  },
  methods: {
    handleSubmit: function() {
      this.submitted = true;
      this.$validator.validate().then(valid => {
        if (valid) {
          this.$store.dispatch("auth/register", this.user).then(
            () => {
              this.$toasted.show("Успешная регистрация!");
              this.$router.push({ name: "Login" });
            },
            err => {
              this.$toasted.show("Ошибка регистрации");
            }
          );
        }
      });
    }
  }
};
</script>

<style scoped>
</style>

