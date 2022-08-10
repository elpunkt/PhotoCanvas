<template>
  <router-view></router-view>
</template>

<script>
import store from '@/store';

const routeGuardAdmin = async (to, from, next) => {
  if (!store.getters.hasAdminAccess) {
    next({name: 'Home'});
  } else {
    next()
  }
}

export default {
  beforeRouteEnter(to, from, next) {
    routeGuardAdmin(to, from, next)
  },
  beforeRouteUpdate(to, from, next) {
    routeGuardAdmin(to, from, next)
  }
}
</script>
