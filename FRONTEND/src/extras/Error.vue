<template>
  <div class="w-full h-screen text-[silver] relative">
    <img
      src="../assets/st3.jpg"
      alt="Error background image"
      class="w-full h-full object-cover opacity-30"
    />
    <div class="w-full text-center absolute top-20">
      <div class="w-full sm:w-10/12 mx-auto md:w-8/12 lg:w-6/12">
        <h2 class="text-5xl sm:text-7xl md:text-9xl mx-auto">404</h2>
        <p class="text-lg sm:text-xl md:text-2xl text-[#e0e0e0] mt-2">
          We could not find that page.
        </p>
        <button
          class="md:px-4 px-2 py-1 sm:py-2 bg-[silver] text-black rounded-full mt-2 hover:bg-[#8b8b8b]"
          @click="goBack()"
        >
          Go Back
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
export default {
  name: "ErrorPage",
  setup() {
    const router = useRouter();

    const goBack = () => {
      router.back();
    };

    return { goBack };
  },
};
</script>

<style></style>
