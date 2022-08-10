<template lang="html">
  <div class="">
    <div>
      <h1>All Photos</h1>
      <div v-for="p in allPhotos" :key="p.id">
        <span><img class="thumbnail" :src="'/uploaded/' + p.filename"></span> |
        <span>{{p.title}}</span> |
        <a class="clickable" @click="deletePhoto(p.id)">Delete</a>
      </div>
    </div>

  </div>
</template>

<script>
import {Api} from "@/api/api.js";

export default {
  data() {
    return {
      allPhotos: []
    }
  },
  methods: {
    deletePhoto(id) {
      Api.deletePhoto(this.$store.state.token, id)
        .then(resp => {
          if (resp.data.state === 'success') {
            this.allPhotos = this.allPhotos.filter((p) => p.id != id)
          }
        })
    }
  },
  mounted() {
    try {
      console.log(this.$store.state.token);
      Api.getAllPhotos(this.$store.state.token)
        .then((response) => {
          this.allPhotos = response.data
        })
    } catch (err) {
      this.$store.commit('addNotification', {content: "Couldn't fetch the list of photos.", color: 'error'})
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
