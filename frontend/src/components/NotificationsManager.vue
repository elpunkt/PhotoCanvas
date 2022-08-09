<template>
  <div>
    <div v-if="currentNotifications.length > 0" class="notification_container">
        <div v-for="note in currentNotifications"
             :key="note.timestamp"
             :class="note.color + '_color'"
             class="single_noticiation">
          <span>{{note.content}}</span>
          <span v-if="note.taskId">
            {{note.color}}
          </span>
        <span class="close_button" @click="removeNotification(note)"><small>x</small></span>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      show: false,
      currentNotifications: new Array()
    }
  },
  methods: {
    removeNotification(notification){
      this.$store.commit('removeNotification', notification)
      this.currentNotifications = this.currentNotifications.filter((note) => note !== notification)
    },
    // testNotification() {
    //   let that = this;
    //   this.$store.commit('addNotification', {content: 'testasd ', color: 'warning', showTime: 4500})
    //   setTimeout(function () {
    //     that.testNotification()
    //   }, 4000);
    // }
  },
  computed: {
    latestNotification() {
      return this.$store.getters.latestNotification
    }
  },
  watch: {
    latestNotification(n) {
      if (n && !this.currentNotifications.includes(n)) {
        this.currentNotifications.push(n)
        let showTime = n.showTime ? n.showTime : 4000
        let that = this;
        setTimeout(function () {
          that.removeNotification(n)
        }, showTime);
      }
    }
  },
}
</script>

<style lang="scss" scoped>
$success: #009900;
$error: #cc0000;
$warning: #ff9900;

 .notification_container {
   position: fixed;
   bottom: 0;
   right: 0;
   max-width: 20vw;
   width: 20vw;
 }
 .single_noticiation {
   padding: 20px;
   border: 5px solid;
   border-radius: 5px;
   margin: 8px 5px;
   position: relative;
 }
 .success_color {
   background-color: $success;
   border-color: lighten($success, 10%)
 }
 .error_color {
   background-color: $error;
   border-color: lighten($error, 10%)
 }
 .warning_color {
   background-color: $warning;
   border-color: lighten($warning, 10%)
 }
 .close_button {
   position:absolute;
   top: 0;
   right: 4px;
   cursor: pointer;
   font-weight: bold;
 }

</style>
