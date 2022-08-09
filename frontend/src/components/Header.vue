<template>
  <div id="header">
    <div class="">
      <router-link :to="{name: 'Photo Upload'}">Upload Photo</router-link>
    </div>
    <div v-if="$store.getters.isLoggedIn">
      <span>Logged in as: {{$store.state.userProfile.email}} </span>
      <button @click="logOut">Log Out</button>
      <router-link :to="{name: 'Slideshow'}">Slideshow</router-link>
    </div>
    <div v-if="$store.getters.hasAdminAccess">
      <router-link :to="{ name: 'Photo List' }">All Photos</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeaderNav',
  methods: {
    async logOut() {
      await this.$store.dispatch('logOut')
    }
  }
}
</script>

<style lang="css" scoped>
</style>
