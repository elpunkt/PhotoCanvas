<template lang="html">
  <div class="">
    <div>
      <h1>All Photos</h1>
      <div v-for="p in allPhotos" :key="p.id">
        <span><img class="thumbnail" :src="'/uploaded/' + p.filename"></span><br>
        <div v-if="$store.getters.hasAdminAccess">
          <v-button :type="'info'" :onClick="rotatePhoto.bind(this, p.id)">Rotate &#x1F504;</v-button>
          <v-button :type="'error'"
                    :onClick="deletePhoto.bind(this, p.id)"
                    :confirmText="'Foto löschen'"
                    :cancelText="'Abbrechen'"
                    needsConfirmation>Delete &#x1F5D1;</v-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {Api} from "@/api/api.js";
import Button from "@/components/Button"

export default {
  components: {
    'v-button' : Button
  },
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
    },
    rotatePhoto(id) {
      Api.rotatePhoto(this.$store.state.token, id)
        .then(resp => {
          console.log(resp);
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
