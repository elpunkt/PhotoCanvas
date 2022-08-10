<template lang="html">
  <div class="">
    <div>
      <h1>All Users</h1>
      <div v-for="u in allUsers" :key="u.id">
        <span>{{u.email}}</span> |
        <span v-if="u.is_superuser">Admin</span><span v-else>User</span> |
        <a class="clickable" @click="deleteUser(u.id)">Delete</a>
      </div>
      <router-link :to="{ name: 'Create User'}">Create</router-link>
    </div>


  </div>
</template>

<script>
import {Api} from "@/api/api.js";

export default {
  data() {
    return {
      allUsers: []
    }
  },
  methods: {
    deleteUser(id) {
      Api.deleteUser(this.$store.state.token, id)
        .then(resp => {
          if (resp.data.state === 'success') {
            this.allUsers = this.allUsers.filter((p) => p.id != id)
          }
        })
    }
  },
  mounted() {
    try {
      Api.getUsers(this.$store.state.token)
        .then((response) => {
          this.allUsers = response.data
        })
    } catch (err) {
      this.$store.commit('addNotification', {content: "Couldn't fetch the list of users.", color: 'error'})
    }

  }
}

</script>

<style lang="scss" scoped>
.clickable {
  cursor: pointer;
}
.thumbnail {
  max-width: 200px;
  max-height: 200px;
}
</style>
