<template>
  <div class="outer-wrap">
    <div class="slider-1-wrap">
      <div class="slider" ref="slider1">
        <div class="slider-item"
             v-for="p in sliderPhotos"
             :key="p.filename"
             ref="sliderItems">
          <div class="img-div" :style="{'background-image': `url(/uploaded/${p.filename})`}">
          </div>
        </div>
        <div class="slider-item"
             v-for="p in sliderPhotos.slice(0,2)"
             :key="`${p.filename}_clone`"
             ref="sliderItemClones">
          <div class="img-div clone" :style="{'background-image': `url(/uploaded/${p.filename})`}">
          </div>
        </div>
      </div>
    </div>
    <div class="slider-2-wrap">
      <div class="slider" ref="slider2">
        <div class="slider-item"
             v-for="p in sliderPhotos"
             :key="p.filename">
          <div class="img-div" :style="{'background-image': `url(/uploaded/${p.filename})`}">
          </div>
        </div>
        <div class="slider-item"
             v-for="p in sliderPhotos.slice(0,1)"
             :key="`${p.filename}_clone`">
          <div class="img-div clone" :style="{'background-image': `url(/uploaded/${p.filename})`}">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {Api} from "@/api/api.js";

export default {
  name: 'Home',
  data() {
    return {
      photos: [],
      scrollPos: 1,
      autoscroll: true,
      sliderWidth: 0
    }
  },
  computed: {
    sliderPhotos() {
      return this.photos
    },
    // sliderWidth() {
    //   return this.$refs.slider1.getBoundingClientRect().width
    // },
    clonesWidth() {
      let width = 0;
      this.$refs.sliderItemClones.forEach(c => {width += c.offsetWidth})
      return width
    }

    // sliderPhotoClones() {
    //   return this.photos
    // }
  },
  methods: {
    connectWebSocket() {
      let that = this
      that.socket = new WebSocket("ws://localhost:8000/new_photos")
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
    scrollUpdate() {
      if (this.autoscroll) {
        this.scrollPos -= 1
      }
      if (this.clonesWidth + this.scrollPos >= this.sliderWidth) {
        window.scrollTo({top: 1});
        this.scrollPos = 1;
        console.log('if 1');
        console.log('scrollPOs', this.scrollPos);
        console.log('sliderWidth', this.sliderWidth);
        console.log('clonesWidth', this.clonesWidth);
      } else if(this.scrollPos <= 0) {
        console.log('if 2');
        console.log('scrollPOs', this.scrollPos);
        console.log('sliderWidth', this.sliderWidth);
        console.log('clonesWidth', this.clonesWidth);

        window.scrollTo({top: this.sliderWidth - this.clonesWidth -1})
        this.scrollPos = this.sliderWidth - this.clonesWidth - 1
      }
      this.$refs.slider1.style.transform = `translateX(${-this.scrollPos}px)`
      this.$refs.slider2.style.transform = `translateX(${this.scrollPos}px)`
      requestAnimationFrame(this.scrollUpdate)
    },
    reCalcSliderWidth() {
      let calcWidth = 0;
      this.$refs.sliderItems.forEach((i) => {
        calcWidth += i.offsetWidth
      });
      this.$refs.slider1.width = calcWidth + 2000
      this.$refs.slider2.width = calcWidth + 2000
      this.sliderWidth = calcWidth + 2000
      console.log(this.$refs.slider2.width);
    }
  },
  mounted() {
    Api.getAllPhotos(this.$store.state.token)
      .then(resp => {
        console.log(resp);
        this.photos = resp.data
      })
      .then(() => {
        this.connectWebSocket()
      })
      .finally(() => {
        this.reCalcSliderWidth()
        this.scrollUpdate()
      })
  },
  updated() {
    this.reCalcSliderWidth()
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
    width: 100vw;
    height: 100vh;
    background-color: black;
  }
  .slider-1-wrap {
    position: fixed;
    top: 10px;
    left: 10px;
    width: 98%;
    height: 49vh;
    overflow: hidden;
  }
  .slider {
    position: absolute;
    top:0;
    left:0;
    height: 100%;
    width: 10000px;
    display: flex;
    will-change: transform;
  }
  .slider-2-wrap {
    position: fixed;
    top: 50vh;
    left: 10px;
    width: 98%;
    height: 49vh;
    overflow: hidden;
  }
  .slider-item {
    position: relative;
    flex: 1;
    overflow: hidden;
  }
  .img-div {
    position: relative;
    left: 1%;
    top: 2.5%;
    width: 98%;
    height:95%;
    background-size: cover;
    background-position: center;
  }

</style>
