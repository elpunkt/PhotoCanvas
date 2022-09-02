<template>
  <div class="outer-wrap">
    <div class="photoItemContainer" v-for="i in photoHtmlItems"
         :key="i.id">
           <img v-if="i.photo"
                class="photoItem"
                :src="`/uploaded/${i.photo.filename}`"
                :key="i.photo.filename"
                :style="{left: i.photo.left + 'px',
                         top: i.photo.top + 'px',
                         zIndex: i.photo.zIndex}">
    </div>
  </div>
  <transition name="fade">
    <div v-if="displayedNewPhoto" class="newPhotoContainer">
      <img :src="`/uploaded/${displayedNewPhoto.filename}`"
           :style="{zIndex: zIndex + 100}">
    </div>
  </transition>
  <div class="statsandcontrols">
    {{displayedPhotos.length}}
    <span style="cursor:pointer; font-size:2em;" @click="addPhoto">&#x1F3B2;</span>
    <div> {{photos.length}} Fotos in der Sammlung</div>
    <div v-if="newPhotos.length > 1">{{newPhotos.length - 1}} Neue Fotos in der Warteschlange</div>
    <!-- <div id="photoSelector">
        <img class="thumbnail"
               v-for="p in photos"
               :src="`/uploaded/${p.filename}`"
               :key="p.filename"
               @click="newPhotos.push(p)"
               :style="[newPhotos.includes(p) ? 'border: 3px solid orange;' : '']">
    </div> -->
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
      newPhotos: [],
      displayedNewPhoto: null,
      readyForNewPhoto: true,
      photoHtmlItems: [],
      zIndex: 1
    }
  },
  watch: {
    photoHtmlItems: {
      handler(oldList, newList) {
        if ((newList.length >= 50) || newList.length == this.photos.length) {
          newList.shift()
          this.displayedPhotos.shift()
        }
      },
      deep: true
    },

    newPhotos: {
      handler(oldList, newList) {
        if ((this.readyForNewPhoto) && (newList.length > 0)) {
          console.log(this.readyForNewPhoto);
          this.readyForNewPhoto = false;
          let that = this
          that.displayedNewPhoto = newList[0]
          setTimeout(() => {
            console.log('first timeout');
            that.displayedNewPhoto = null;
            setTimeout(() => {
              console.log('inner timeout');
              that.readyForNewPhoto = true;
              that.newPhotos.shift()
            }, 2500);
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
          // that.$store.commit('addNotification', { content: 'Neues Foto', color: 'success' })
        } else if (data.action === 'delete') {
          that.photos = that.photos.filter((p) => p.filename != data.photo.filename)
          // that.$store.commit('addNotification', { content: 'Ein Foto wurde entfernt.', color: 'success' })
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
    addPhoto() {
      let notDisplayed = this.photos.filter((p) => !(this.displayedPhotos.includes(p.filename)))
      let random = Math.floor(Math.random() * notDisplayed.length);
      let randomPhoto = notDisplayed[random]
      randomPhoto.left = Math.floor(Math.random()* this.maxLeft)
      randomPhoto.top = Math.floor(Math.random()* this.minTop)
      // randomPhoto.maxWidth = Math.floor(Math.random()* (120 - 100 +1) + 100)
      // randomPhoto.maxHeight = Math.floor(Math.random()* (120 - 100 +1) + 100)
      randomPhoto.zIndex = this.zIndex
      this.zIndex ++
      this.photoHtmlItems.push({photo: randomPhoto})
      this.displayedPhotos.push(randomPhoto.filename)
    },
    addEveryXseconds(X){
      this.addPhoto()
      let that = this;
      setTimeout(() => {
        that.addEveryXseconds(X)
      }, X * 1000)
    },
    calcDimensions() {
      let width = window.innerWidth;
      let height = window.innerHeight;
      this.maxLeft = width/3*2
      this.minTop = height/2
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
        this.addEveryXseconds(4)
      })
  },
  beforeUnmount() {
    this.socket.close()
  }

}
</script>

<style lang="scss">
#photoSelector {
    background: black;
    z-index: 9999999999999999;
    position: fixed;
    top: 0;
    right: 0;
    width: 10vw;
    height: 100vh;
    overflow-y: scroll;
    img {
      max-height: 10vh;

    }
  }
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

  .statsandcontrols {
    z-index: 99999999999999;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    color: white;
    position: fixed;
    bottom: 0;
    right: 0;
    font-size: 0.8rem;
    font-family: Abel, sans-serif;
  }

  .photoItem {
    position: fixed;
    max-width: 30vw;
    max-height: 50vh;
    border: 5px solid white;
    filter: drop-shadow(0 0 0.3rem white);
  }

  .photoItemContainer {
    width: 100vw;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    background-color: rgba(0,0,0,0.04);
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
