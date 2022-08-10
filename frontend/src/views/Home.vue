<template lang="html">
  <div class="outer-wrap">
    <div class="inner-wrap">
      <div class="content">
        <div class="abschnitt" v-if="$store.getters.isLoggedIn">
          <span>Eingeloggt als: {{$store.state.userProfile.email}} </span>
          <button @click="logOut">Log Out</button>
        </div>
        <div class="abschnitt" v-else>
          <span>Nicht eingeloggt</span>
          <button @click="$router.push({ name: 'Login'})" >Zum Login</button>
        </div>
        <div class="abschnitt">
          <button @click="$router.push({ name: 'Photo Upload'})">Foto hochladen&#x1F5BC;</button>
          <button @click="$router.push({ name: 'Slideshow'})">Zur Fotowand (Passwort benötigt)</button>
        </div>
        <div class="abschnitt" v-if="$store.getters.hasAdminAccess">
          <button @click="$router.push({ name: 'Photo List' })">Fotos löschen</button>
          <button @click="$router.push({ name: 'User List'})">User hinzufügen</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Home',
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
button {
  background-color: $buttoncol;
  cursor: pointer;
  border: 1px solid #ccc;
  padding: 2px 4px;
  display: flex;
  justify-content: center;
  align-content: center;
  flex-direction: column;
  text-decoration: none;
  min-width: 300px;
  min-height: 60px;
  font-size: 2em;
  &:disabled {
    cursor:not-allowed;
  }
  &:hover {
    background-color: darken($buttoncol,10)
  }
}

</style>
