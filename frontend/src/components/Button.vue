<template>
<button @click.prevent="_onClick"
        class="btn"
        :style="style"
        :disabled="disabled"
        :class="[
          type && 'btn-' + type,
          size && 'btn-' + size
                ]">
  <slot>Button</slot>
</button>
<centeredDiv v-if="showConfirmButton">
  <div class="confirmButtonWrapper">
    <div v-if="confirmQuestion">{{confirmQuestion}}</div>
    <button class="btn btn-success" @click.prevent="confirmClick">{{confirmText}}</button>
    <button class="btn btn-warning" @click.prevent="cancelClick">{{cancelText}}</button>
  </div>
</centeredDiv>
</template>
<script>
import centeredDiv from "@/components/layout/CenteredDiv";

export default {
  components: {
    centeredDiv
  },
  props: {
    style: {
      type: Object
    },
    onClick: {
      type: Function,
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    },
    confirmQuestion: {
      type: String
    },
    confirmText: {
      type: String,
      default: "confirm"
    },
    cancelText: {
      type: String,
      default: "cancel"
    },
    type: {
      type: String,
    },
    size: {
      type: String,
    },
    needsConfirmation: Boolean,
  },
  data() {
    return {
      showConfirmButton: false
    }
  },
  methods: {
    _onClick() {
      if (this.needsConfirmation) {
        this.showConfirmButton = true;
      } else {
        this.onClick()
      }
    },
    confirmClick() {
      this.onClick()
    },
    cancelClick() {
      this.showConfirmButton = false;
    }
  }
}
</script>
<style lang="scss" scoped>

$neutralCol: white;
$successCol: #2ecc71;
$infoCol: #3498db;
$warningCol: #f1c40f;
$errorCol: #e74c3c;


@mixin button-bg($bg) {
  background-color: $bg;
  border-color: darken($bg, 2%);
  &:hover {
    background:darken($bg,8%);
    transition: all 0.3s ease;
  }
  &:active {
    background:darken($bg,25%);
  }
  &:disabled {
    background:lighten($bg, 20%);
    cursor: not-allowed;
  }
}

.btn {
 color:black;
 background-color: $neutralCol;
 border-color: darken($neutralCol, 2%);
 text-decoration:none;
 padding: 0.25rem 0.5rem;
 border-radius:0.1rem;
 font-family: -system-ui, sans-serif;
 font-size:1.4em;
 white-space: nowrap;
 cursor: pointer;
 line-height: 1.2;
 &:hover {
   background-color: darken($neutralCol, 8%)
 }
 &:active {
   background:darken($neutralCol,25%);
 }
 &:disabled {
   background:darken($neutralCol, 50%);
   cursor: not-allowed;
   color: $neutralCol;
   opacity: 0.8;
 }

 &-max {
   font-size: 2.5em;
 }
 &-large {
   font-size: 2em;
 }
 &-small {
   font-size: 1.1em;
   padding: 0.2rem 0.3rem;
 }
 &-mini {
   font-size: 0.9em;
   padding: 0.2rem 0.3rem;
 }
}

.btn-success {
   @include button-bg($successCol);
}

.btn-info{
   @include button-bg($infoCol);
}

.btn-warning{
   @include button-bg($warningCol);
}

.btn-error {
   @include button-bg($errorCol);
}

.confirmButtonWrapper {
  > button {
    margin: 10px;
  }
}
</style>
