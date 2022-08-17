<template>
  <div class="outer-wrap" :style="{gridTemplateRows: 'repeat(' + this.rows + ', 1fr)', gridTemplateColumns: 'repeat(' + this.cols + ', 1fr)'}">
    <div v-for="i in photoGridItems"
         class="griditem"
         :key="i.id">
         <transition name="fade">
           <img v-if="i.photo"
                :src="`/uploaded/${i.photo.filename}`"
                :key="i.photo.filename"
                :style="{maxHeight: i.photo.maxHeight + '%',
                         maxWidth: i.photo.maxWidth + '%',
                         marginTop: i.photo.marginTop + 'px',
                         marginLeft: i.photo.marginLeft + 'px',
                         zIndex: i.photo.zIndex}">
         </transition>
    </div>
  </div>
  <transition name="fade">
    <div v-if="displayedNewPhoto" class="newPhotoContainer">
      <img :src="`/uploaded/${displayedNewPhoto.filename}`"
           :style="{zIndex: zIndex + 100}">
    </div>
  </transition>
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
      newPhotos: [],
      displayedNewPhoto: null,
      readyForNewPhoto: true,
      photoGridItems: [],
      cols: 0,
      rows: 0,
      zIndex: 1
    }
  },
  watch: {
    newPhotos: {
      handler(oldList, newList) {
        if (this.readyForNewPhoto) {
          this.readyForNewPhoto = false;
          let that = this
          that.displayedNewPhoto = newList[0]
          setTimeout(() => {
            that.displayedNewPhoto = null;
            setTimeout(() => {
              that.readyForNewPhoto = true;
              that.newPhotos.shift()
            }, 3000);
          }, 6000);
        }
      },
      deep: true
    }
  },
  methods: {
    connectWebSocket() {
      let that = this
      that.socket = new WebSocket(`${wsUrl}/new_photos`)
      that.socket.onmessage = function(e) {
        let data = JSON.parse(e.data)
        if (data.action === 'add') {
          that.photos.push(data.photo)
          that.newPhotos.push(data.photo)
          console.log(that.newPhotos);
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
        //random Margins in range -70 to 70
        randomPhoto.marginTop = Math.floor(Math.random()*140-70)
        randomPhoto.marginLeft = Math.floor(Math.random()*140-70)
        // ranom MaxDimensions in range 100 to 120
        randomPhoto.maxWidth = Math.floor(Math.random()* (120 - 100 +1) + 100)
        randomPhoto.maxHeight = Math.floor(Math.random()* (120 - 100 +1) + 100)
        randomPhoto.zIndex = this.zIndex
        this.zIndex ++
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

    },
    calcDimensions() {
      this.photoGridItems = [];
      let width = window.innerWidth;
      let height = window.innerHeight;
      this.cols = Math.floor(width/480);
      this.rows = Math.floor(height/480);
      if (this.cols === 0) {
        this.cols = 1;
      }
      if (this.rows === 0) {
        this.rows = 1;
      }
      for (let col=0; col<this.cols; col ++) {
        for (let row=0; row<this.rows; row++) {
          this.photoGridItems.push({photo:null})
        }
      }
    }
  },
  mounted() {
    this.calcDimensions()
    Api.getAllPhotos(this.$store.state.token)
      .then(resp => {
        this.photos = resp.data
      })
      .then(() => {
        this.connectWebSocket()
      })
      .finally(() => {
        this.photoGridItems.forEach((p) => {
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
  }
  .newPhotoContainer {
    position: absolute;
    left: 50%;
    top: 50%;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    padding: 30px;
    border: 5px solid #ff8300;
    border-radius: 10px;
    background-color: black;
    img {
      max-height: 90vh;
      max-width: 90vw;
    }
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

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 3s ease-in-out;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
</style>
