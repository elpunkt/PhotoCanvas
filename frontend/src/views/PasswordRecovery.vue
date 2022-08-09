<template lang="html">
  <div class="">
    <h5>Password Recovery</h5>
    <p>A password recovery email will be sent to the registered account</p>
    <form @keyup.enter="submit">
      <input v-model="email" type="email" name="email" placeholder="Email" required>
      <button @click="submit" type="button" name="button">Recover Password</button>
    </form>

  </div>
</template>

<script>
export default {
  data() {
    return {
      email: null
    }
  },
  methods: {
    submit() {
      this.$store.dispatch("passwordRecovery", this.email)
    }
  }
}
</script>

<style lang="css" scoped>
</style>
