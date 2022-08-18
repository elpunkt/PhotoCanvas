<template lang="html">
  <centeredDiv>
    <form @keyup.enter="submit">
      <div class="">
        <div class="">Email</div>
        <input v-model="email" type="text" name="email">
      </div>
      <div class="">
        <div class="">is admin?</div>
        <input v-model="isSuperuser" type="checkbox" name="is_superuser">
      </div>
      <div class="">
        <div class="">is active?</div>
        <input v-model="isActive" type="checkbox" name="is_superuser">
      </div>
      <div class="">
        <div class="">New Password</div>
        <input v-model="password1" type="password">
      </div>
      <div class="">
        <div class="">Confirm new Password</div>
        <input v-model="password2" type="password">
      </div>
      <btn :onClick="submit"
           :size="'small'"
           :type="'success'"
           :style="{marginTop:'10px'}">Submit</btn>
    </form>
  </centeredDiv>
</template>

<script>
import { Api } from '@/api/api';
import centeredDiv from '@/components/layout/CenteredDiv'
import Button from '@/components/Button'

export default {
  components: {
    'btn': Button,
    centeredDiv
  },
  data() {
    return {
      email: '',
      isActive: true,
      isSuperuser: false,
      password1: null,
      password2: null
    }
  },
  methods: {
    submit() {
      let newProfile = {}
      if (this.password1 && this.password1 === this.password2) {
        newProfile.password = this.password1;
        newProfile.email = this.email;
        newProfile.is_active = this.isActive;
        newProfile.is_superuser = this.isSuperuser;
        console.log(newProfile);
        Api.createUser(this.$store.state.token, newProfile)
        .then(() => {
          this.$store.commit('addNotification', {content: "User created", color: 'success'})
          this.$router.push({name: 'User List'})
        })
        .catch((err) => {
          if (err.response.status === 400) {
            this.$store.commit('addNotification', {content: err.response.data.detail, color: 'error'})
          } else {
            err.response.data.detail.map((e) => {
              this.$store.commit('addNotification', { content: e.msg, color: 'error'})
            })
          }
        })
      } else {
        this.$store.commit('addNotification', {content: "Password do not match.", color: 'error'})
      }
    }
  }
}
</script>

<style lang="css" scoped>
</style>
