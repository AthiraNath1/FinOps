<script>
export default {
  data() {
    return {}
  }
}
</script>
<template>
  <v-footer padless class="footer">
    <v-col class="text-center" cols="12" bg-teal>
      <!-- <span class="content">© Mercedes Benz {{ new Date().getFullYear() }}</span> -->
    </v-col>
  </v-footer>
</template>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  background: var(--blue-blue-25, #014880);
  width: 100%;
  padding: 0;
  flex-shrink: 0;
  flex: unset;
  z-index: 999;
}

.content {
  color: var(--test-white, #fff);
  font-family: MB Corpo S Text WEB;
  font-size: 14px;
  font-style: normal;
  font-weight: 700;
  line-height: 14px;
}
</style>