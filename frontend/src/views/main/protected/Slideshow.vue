<template>
  <div class="outer-wrap">
    <div v-for="i in photoGrids"
         class="griditem"
         :class="`girditem${i.id}`"
         :key="i.id">
         <transition name="fade">
           <img v-if="i.photo"
                :src="`/uploaded/${i.photo.filename}`"
                :key="i.photo.filename"
                :style="{maxHeight: i.photo.maxHeight + '%',
                         maxWidth: i.photo.maxWidth + '%',
                         marginTop: i.photo.marginTop + 'px',
                         marginLeft: i.photo.marginLeft + 'px'}">
         </transition>
    </div>
  </div>
</template>

<script>
import {Api} from "@/api/api.js";
import {wsUrl} from '@/env'

export default {
  name: 'Home',
  data() {
    return {
      photos: [],
      displayedPhotos: [],
      photoGrids: [{id: 1, photo: null}, {id: 2, photo: null}, {id: 3, photo: null}, {id: 4, photo: null}, {id: 5, photo: null},{id: 6, photo: null},{id: 7, photo: null},{id: 8, photo: null}]
    }
  },
  methods: {
    connectWebSocket() {
      let that = this
      that.socket = new WebSocket(`${wsUrl}/new_photos`)
      that.socket.onmessage = function(e) {
        let data = JSON.parse(e.data)
        if (data.action === 'add') {
          that.photos.unshift(data.photo)
          that.$store.commit('addNotification', { content: 'Neues Foto', color: 'success' })
        } else if (data.action === 'delete') {
          that.photos = that.photos.filter((p) => p.filename != data.photo.filename)
          that.$store.commit('addNotification', { content: 'Ein Foto wurde entfernt.', color: 'success' })
        } else {
          console.log('Websocket received unknown action "' + data.action + '".');
        }
      }
      that.socket.onclose = function() {
        that.$store.commit('addNotification', { content: 'Verbindung zum Server verloren.', color: 'error', showTime: 2000 })
        console.log('WebSocket connection is closed. Attem,pting reconnect.');
        setTimeout(function() {that.connectWebSocket()}, 1000)
      }
      that.socket.onerror = function(err) {
        console.log('WebSocket encountered error: ' + err.message + 'Closing Websocket.');
        that.socket.close()
      }
    },
    replacePhoto(p) {
      let oldPhoto = p.photo
      let random = Math.floor(Math.random() * this.photos.length);
      let randomPhoto = this.photos[random]
      if (!(this.displayedPhotos.includes(randomPhoto.filename)) && !(randomPhoto === oldPhoto)) {
        //random Margins in range -100 to 100
        randomPhoto.marginTop = Math.floor(Math.random()*200-100)
        randomPhoto.marginLeft = Math.floor(Math.random()*200-100)
        // ranom MaxDimensions in range 100 to 120
        randomPhoto.maxWidth = Math.floor(Math.random()* (120 - 100 +1) + 100)
        randomPhoto.maxHeight = Math.floor(Math.random()* (120 - 100 +1) + 100)

        p.photo = randomPhoto
        this.displayedPhotos.push(randomPhoto.filename)
        if (oldPhoto) {
          this.displayedPhotos.splice(this.displayedPhotos.indexOf(oldPhoto.filename), 1)
        }
        var replaceIn = Math.floor(Math.random() * (20 - 10 + 1) + 10)
      } else {
        replaceIn = 1
      }
      // console.log(replaceIn);
      let that = this;
      setTimeout(function () {
        that.replacePhoto(p)
      }, replaceIn*1000);

    }
  },
  mounted() {
    Api.getAllPhotos(this.$store.state.token)
      .then(resp => {
        this.photos = resp.data
      })
      .then(() => {
        this.connectWebSocket()
      })
      .finally(() => {
        this.photoGrids.forEach((p) => {
          this.replacePhoto(p)
        });

      })
  },
  beforeUnmount() {
    this.socket.close()
  }

}
</script>

<style lang="scss">
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
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(12, 1fr);
  }

  .griditem {
    display: grid;
    justify-items: center;
    align-items: center;
    position: relative;
    & img {
      position: absolute;
      top: 0;
      max-width: 100%;
      max-height: 100%;
    }
  }

  .girditem1 {
    grid-column-start: 0;
    grid-column-end: 2;
    grid-row-start:1;
    grid-row-end:5;
    // background-color: red;
  }

  .girditem2 {
    grid-column-start: 0;
    grid-column-end: 2;
    grid-row-start:5;
    grid-row-end:9;
    // background-color: blue;
  }

  .girditem3 {
    grid-column-start: 0;
    grid-column-end: 2;
    grid-row-start:9;
    grid-row-end:13;
    // background-color: green;
  }

  .girditem4 {
    grid-column-start: 2;
    grid-column-end: 3;
    grid-row-start:1;
    grid-row-end:7;
    // background-color: green;
  }

  .girditem5 {
    grid-column-start: 3;
    grid-column-end: 4;
    grid-row-start:1;
    grid-row-end:7;
    // background-color: blue;
  }

  .girditem6 {
    grid-column-start: 2;
    grid-column-end: 4;
    grid-row-start:7;
    grid-row-end:13;
    // background-color: red;
  }

  .girditem7 {
    grid-column-start: 4;
    grid-column-end: 5;
    grid-row-start:1;
    grid-row-end:8;
    // background-color: green;
  }

  .girditem8 {
    grid-column-start: 4;
    grid-column-end: 5;
    grid-row-start:8;
    grid-row-end:13;
    // background-color: blue;
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 3s ease-in-out;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
</style>
