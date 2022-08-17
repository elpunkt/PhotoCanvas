<template lang="html">
  <centeredDiv>
      <div class="content">
        <div class="abschnitt" v-if="$store.getters.isLoggedIn">
          <span>Eingeloggt als: {{$store.state.userProfile.email}} </span>
          <btn :onClick="logOut">Log Out</btn>
        </div>
        <div class="abschnitt" v-else>
          <span>Nicht eingeloggt</span>
          <btn :onClick="$router.push.bind(this, { name: 'Login'})" >Zum Login</btn>
        </div>
        <div class="abschnitt">
          <btn :onClick="$router.push.bind(this, { name: 'Photo Upload'})">Foto hochladen&#x1F5BC;</btn>
        </div>
        <div class="abschnitt" v-if="$store.getters.isLoggedIn">
          <btn :onClick="$router.push.bind(this, { name: 'Slideshow'})">Zur Fotowand</btn>
          <btn :onClick="$router.push.bind(this, { name: 'Photo List' })">Alle Fotos</btn>
        </div>
        <div class="abschnitt" v-if="$store.getters.hasAdminAccess">
          <btn :onClick="$router.push.bind(this, { name: 'User List'})">User hinzufügen</btn>
        </div>
      </div>
  </centeredDiv>
</template>

<script>
import centeredDiv from '@/components/layout/CenteredDiv'
import Button from '@/components/Button'

export default {
  name: 'Home',
  components: {
    'btn': Button,
    centeredDiv,
  },
  methods: {
    async logOut() {
      await this.$store.dispatch('logOut')
    }
  }
}
</script>

<style lang="scss" scoped>
.abschnitt {
  display: flex;
  flex-direction: column;
  padding: 5px;
  border-bottom: 3px solid black
}
.content {
  display: flex;
  flex-direction: column;
}

$buttoncol: white;

</style>
