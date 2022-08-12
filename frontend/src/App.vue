<template>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💐</text></svg>">
  <Header/>
  <router-view/>
  <NotificationsManager/>
  <div class="credits">
    by <a href="https://luona.dev">[luona]</a> development
  </div>
</template>
<script>
import Header from '@/components/Header.vue';
import NotificationsManager from '@/components/NotificationsManager.vue';
export default {
  components: {
    Header,
    NotificationsManager
  },
  created() {
    this.$store.dispatch('checkLoggedIn')
  },
  mounted() {
    document.title= 'Merle & Jan';
  }
}
</script>


<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Abel&family=Roboto&display=swap');

*{
  margin: 0;
  padding: 0;
  box-sizing:border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.credits {
  font-size: 0.8rem;
  background-color: black;
  padding: 3px;
  margin-left: 5px;
  position: fixed;
  bottom: 0;
  left: 0;
  color: white;
  a {
    color: white;
    text-decoration: none;
    color: gold;
    font-family: Abel, sans-serif;
  }
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
