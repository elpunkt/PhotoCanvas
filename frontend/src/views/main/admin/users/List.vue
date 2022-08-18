<template lang="html">
  <centeredDiv>
        <h1>All Users</h1>
        <div class="list">
          <div class="list-row" v-for="u in allUsers" :key="u.id">
            <span>{{u.email}}</span>
            <span v-if="u.is_superuser">Admin</span><span v-else>User</span>
            <btn :onClick="deleteUser.bind(this, u.id)"
            :type="'error'"
            :size="'mini'"
            needsConfirmation>Delete &#x1F5D1;</btn>
          </div>
        </div>
        <btn :type="'success'"
             :size="'small'"
             :onClick="$router.push.bind(this, { name: 'Create User'})">Create</btn>
  </centeredDiv>
</template>

<script>
import {Api} from "@/api/api.js";
import centeredDiv from '@/components/layout/CenteredDiv'
import Button from '@/components/Button'

export default {
  components: {
    'btn': Button,
    centeredDiv
  },
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
.list {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
.list-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2px;
  align-items: center;
  min-width: 300px;
}
</style>
