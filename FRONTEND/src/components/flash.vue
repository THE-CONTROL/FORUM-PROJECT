<template>
  <div
    v-if="flash.msg"
    class="w-full text-xs py-0.5 sm:text-sm md:text-base bg-[#141414] border rounded-b-3xl flex flex-row justify-between"
    :class="
      flash.bool
        ? 'text-green-700 border-green-700'
        : 'text-red-700 border-red-700'
    "
  >
    <h4 class="mx-5">{{ flash.msg }}</h4>
    <button
      class="mx-5"
      :class="flash.bool ? 'hover:text-green-900' : 'hover:text-red-900'"
      @click="clearFlash()"
    >
      <fa :icon="['fas', 'xmark']" />
    </button>
  </div>
</template>

<script>
export default {
  name: "FlashComp",
  props: {
    flash: Object,
    clearFlash: Function,
  },
};
</script>

<style></style>
