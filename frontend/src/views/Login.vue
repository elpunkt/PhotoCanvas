<template lang="html">
  <div class="login">
    <form>
      <input v-model="email" name="login" label="Login" type="text" placeholder="Email">
      <input v-model="password" name="password" label="Password" type="password" placeholder="Password">
      <button @click.prevent="submit">Login</button>
      <router-link :to="{ name: 'PasswordRecovery'}">recover password</router-link>
    </form>
  </div>
</template>

<script>

export default {
  name: 'Login',
  data() {
    return {
      email: null,
      password: null,
    }
  },
  methods: {
    submit() {
      this.$store.dispatch('logIn', {username: this.email, password: this.password})
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
