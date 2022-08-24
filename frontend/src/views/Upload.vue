<template lang="html">
  <centeredDiv>
    <div class="content">
      <label for="file-upload" class="file-upload-label">Fotos auswählen &#x1F5BC;</label>
      <input id="file-upload" type="file" ref="file" @change="fileChanged" multiple><br>
      <btn id="customButton"
           :size="'large'"
           :type="'success'"
           :onClick="uploadPhoto"
           :disabled="!fileSelected"
           :style="{minWidth: '300px'}"
           ><span><span v-if="!fileSelected">&#x1F6A7;---&#x1F6A7;---&#x1F6A7;</span><span v-else>&#x1F389; und ab dafür! &#x1F37E;</span></span></btn>
    </div>
  </centeredDiv>
  <div v-if="isLoading" class="loadingscreen">

  </div>
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
      fileSelected: false,
      isLoading: false
    }
  },
  methods: {
    uploadPhoto() {
      this.isLoading = true
      var promises = Array.from(this.$refs.file.files).map((f) => {
        return Api.uploadPhoto(f)
          .then((r) => {
            this.$store.commit('addNotification', { content: r.data.message, color: r.data.state})
          })
      })
      Promise.all(promises).then(() => {
        this.$refs.file.value = null;
        this.isLoading = false;
        this.fileChanged()
      })
    },
    fileChanged() {
      if (this.$refs.file.files.length > 0) {
        this.fileSelected = true;
      } else {
        this.fileSelected = false;
      }
    }
  },
}
</script>

<style lang="scss" scoped>
.loadingscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: white;
  opacity: 0.5;
  cursor: wait;
}

.content {
  color: black;
  background-color: white;
  text-align: center;
}

input[type="file"] {
    display: none;
}

.file-upload-label {
    border: 2px solid #ccc;
    display: flex;
    padding: 0.25rem 0.5rem;
    border-radius: 0.1rem;
    cursor: pointer;
    min-width: 300px;
    min-height: 60px;
    justify-content: center;
    align-content: center;
    flex-direction: column;
    font-size: 2em;
    &:hover {
      background-color: darken(#2ecc71, 8%)
    }
}
</style>
