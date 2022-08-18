<template>
  <div class="outerWrap">
    <div class="innerWrap">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css" scoped>
 .outerWrap {
   position: fixed;
   top: 0;
   left: 0;
   width: 100vw;
   height: 100vh;
   background-color: rgba(255,255,255,0.8);
   cursor: not-allowed;
   display: flex;
   justify-content: center;
   align-items: center;
 }
 .innerWrap {
   background-color: white;
   padding: 30px;
   border: 5px solid #ff8300;
   border-radius: 10px;
   cursor: default;
 }
</style>
