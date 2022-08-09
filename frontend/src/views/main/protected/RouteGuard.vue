<template>
  <router-view></router-view>
</template>

<script>
import store from '@/store';

const routeGuardLoggedIn = async (to, from, next) => {
  if (!store.getters.isLoggedIn) {
    next({name: 'Login'});
  } else {
    next()
  }
}

export default {
  beforeRouteEnter(to, from, next) {
    routeGuardLoggedIn(to, from, next)
  },
  beforeRouteUpdate(to, from, next) {
    routeGuardLoggedIn(to, from, next)
  }
}
</script>
