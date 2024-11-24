<template>
  <div class="container mt-0 p-0">
    <BankSearch />
  </div>
</template>

<script>
import BankSearch from "@/components/BankSearch.vue";

export default {
  name: "MapView",
  components: {
    BankSearch,
  },
};
</script>

<style>
.box-container {
  display: flex;
  justify-content: center;
}

</style>
