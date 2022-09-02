<template>
  <div class="w-full h-screen relative text-white">
    <img
      class="w-full h-screen object-cover opacity-30"
      src="../assets/ldImg.jpg"
      alt="Landing Page Background"
    />
    <div class="w-full mt-48 md:mt-36 absolute top-0 left-0">
      <div class="m-auto text-center px-4">
        <h1
          class="text-4xl sm:text-5xl md:text-6xl font-semibold text-blue-400"
        >
          A Reliable Information<br />
          <span class="text-blue-100">Community</span>
        </h1>
        <p class="sm:text-lg mt-4 text-blue-100">
          Get Information about the latest in technology, sports, health etc.
        </p>
        <div class="w-full flex flex-row gap-2 sm:gap-4 justify-center mt-5">
          <router-link
            v-for="(li, index) in lis"
            :key="index"
            :to="li.to"
            class="rounded-lg p-1 md:text-base sm:p-1 md:p-2 font-semibold bg-gradient-to-b from-blue-900 to-blue-500 hover:from-blue-700 to bg-blue-300"
          >
            {{ li.name }}</router-link
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onBeforeMount } from "@vue/runtime-core";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "LandingPage",
  setup() {
    const router = useRouter();
    const route = useRoute();
    const lis = [
      { name: "Login", to: "/login" },
      { name: "Register", to: "/register" },
    ];

    onBeforeMount(() => {
      if (localStorage.getItem("ref")) {
        router.push({
          name: "LoginPage",
          query: {
            ...route.query,
          },
        });
      }
    });

    return { lis };
  },
};
</script>

<style></style>
