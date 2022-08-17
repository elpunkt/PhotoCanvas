<template lang="html">
  <centeredDiv>
    <form class="content">
      <input v-model="email" name="login" label="Login" type="text" placeholder="Email">
      <input v-model="password" name="password" label="Password" type="password" placeholder="Password">
      <btn :type="'success'" :disabled="working" :onClick="submit">Login</btn>
    </form>
  </centeredDiv>
</template>

<script>
import centeredDiv from '@/components/layout/CenteredDiv'
import Button from '@/components/Button'

export default {
  name: 'Login',
  components: {
    'btn': Button,
    centeredDiv
  },
  data() {
    return {
      email: null,
      password: null,
      working: false,
    }
  },
  methods: {
    submit() {
      this.working = true;
      this.$store.dispatch('logIn', {username: this.email, password: this.password})
      this.working = false;
    }
  }
}
</script>

<style lang="scss" scoped>
input {
  height: 40px;
  margin-bottom: 5px;
  font-size: 20px;
}

.content {
  display: flex;
  flex-direction: column;
}
</style>
