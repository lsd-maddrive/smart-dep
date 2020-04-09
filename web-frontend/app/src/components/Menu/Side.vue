<template>
  <div class="sidebar">
    <div class="sidebar-backdrop" @click="closeSidebarPanel" v-if="isActive"></div>
    <transition name="slide">
      <div v-if="isActive" class="sidebar-panel">
        <div class="slot-wrapper">
          <slot></slot>
        </div>
      </div>
    </transition>
  </div>
</template>
<script>
export default {
  data: () => ({}),
  computed: {
    isActive() {
      return this.$store.state.isSidemenuOpen;
    }
  },
  methods: {
    closeSidebarPanel() {
      this.$store.commit("toggleSidemenu");
    }
  }
};
</script>
<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.2s ease;
}

.slide-enter,
.slide-leave-to {
  transform: translateX(-100%);
  transition: all 150ms ease-in 0s;
}

.sidebar-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;
  cursor: pointer;
}

.sidebar-panel {
  overflow-y: auto;
  background-color: rgb(34, 34, 34);
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  z-index: 1;
  padding: 3rem 20px 2rem 20px;
  width: 300px;
}

.slot-wrapper {
  width: 100%;
}
</style>