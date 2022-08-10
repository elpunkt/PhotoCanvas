<template lang="html">
  <div class="outer-wrap">
    <div class="inner-wrap">
      <div class="content">
        <label for="file-upload" class="file-upload-label">Foto auswählen &#x1F5BC;</label>
        <input id="file-upload" type="file" ref="file" @change="fileChanged"><br>
        <!-- <input type="text" v-model="title" placeholder="Titel/Beschreibung (optional)"><br> -->
        <button id="upload-button"
                @click="uploadPhoto"
                :disabled="!selectedFile"><span><span v-if="!selectedFile">&#x1F6A7;---&#x1F6A7;---&#x1F6A7;</span><span v-else><span>und ab dafür!</span> &#x1F470;❤️&#x1F935;</span></span></button>
        {{fileSelected}}
      </div>
    </div>
  </div>
</template>

<script>
import {Api} from "@/api/api.js";

export default {
  data() {
    return {
      title: null,
      selectedFile: null
    }
  },
  methods: {
    uploadPhoto() {
      let f = this.selectedFile;
      this.selectedFile = null;
      Api.uploadPhoto(f, this.title)
        .then(() => {
          this.$store.commit('addNotification', { content: 'Das Foto wurde hochgeladen und wird in Kürze in der Diashow erscheinen', color: 'success'})
          this.$refs.file.value = null
          this.selectedFile = null
        })
    },
    fileChanged() {
      this.selectedFile = this.$refs.file.files[0]
    }
  },
}
</script>

<style lang="scss" scoped>
#header {
  display: none;
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
}

input[type="file"] {
    display: none;
}
$buttoncol: white;

.file-upload-label {
    border: 1px solid #ccc;
    display: flex;
    padding: 6px 12px;
    cursor: pointer;
    min-width: 300px;
    min-height: 60px;
    justify-content: center;
    align-content: center;
    flex-direction: column;
    font-size: 2em;
    &:hover {
      background-color: lighten(green,50)
    }
}

#upload-button {
  background-color: $buttoncol;
  cursor: pointer;
  border: 1px solid #ccc;
  padding: 6px 12px;
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
    background-color: darken($buttoncol,10);
  }
  &:hover {
    background-color: darken($buttoncol,10);
  }
}
</style>
