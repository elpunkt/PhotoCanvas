<template lang="html">
  <div class="outer-wrap">
    <div class="inner-wrap">
      <form class="content">
        <input v-model="email" name="login" label="Login" type="text" placeholder="Email">
        <input v-model="password" name="password" label="Password" type="password" placeholder="Password">
        <button id="login-button" @click.prevent="submit">Login</button>
      </form>
    </div>
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
.outer-wrap {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: black;
}
.inner-wrap {
  background-color: white;
  position: absolute;
  left: 50%;
  top: 50%;
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  padding: 30px;
  border: 5px solid #ff8300;
  border-radius: 10px;
}

.content {
  color: black;
  background-color: white;
  text-align: center;
  display: flex;
  flex-direction: column;
}

$buttoncol: white;

#login-button {
  background-color: $buttoncol;
  cursor: pointer;
  border: 1px solid #ccc;
  padding: 2px 4px;
  display: flex;
  justify-content: center;
  align-content: center;
  flex-direction: column;
  text-decoration: none;
  min-width: 50px;
  min-height: 30px;
  &:disabled {
    cursor:not-allowed;
  }
  &:hover {
    background-color: darken($buttoncol,10)
  }
}

</style>
