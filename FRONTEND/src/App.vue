<template>
  <div class="text-[#eeeeee]">
    <IntroPage v-if="!showApp" />
    <div
      v-else
      class="bg-black min-h-screen relative max-w-screen overflow-clip"
    >
      <NavBar
        :loggedIn="loggedIn"
        :setFlash="setFlash"
        :setLoggedIn="setLoggedIn"
        :logOut="logOut"
        :user="user"
      />
      <FlashComp :flash="flash" :clearFlash="clearFlash" />
      <router-view
        :setFlash="setFlash"
        :setLoggedIn="setLoggedIn"
        :logOut="logOut"
        :loggedIn="loggedIn"
        :user="user"
        v-slot="{ Component }"
      >
        <transition name="fade">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script>
import NavBar from "./components/navBar.vue";
import FlashComp from "./components/flash.vue";
import IntroPage from "./extras/intro.vue";
import { ref } from "@vue/reactivity";
import { onBeforeMount } from "@vue/runtime-core";
import { useRouter, useRoute } from "vue-router";
import useComp1 from "./mix/data.js";

export default {
  components: {
    NavBar,
    FlashComp,
    IntroPage,
  },
  setup() {
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const loggedIn = ref(false);
    const user = ref({});
    const showApp = ref(false);

    const showAppFunc = () => {
      showApp.value = true;
    };

    const flash = ref({
      msg: "",
      bool: false,
    });

    const setFlash = (msg, bool) => {
      flash.value.msg = msg;
      flash.value.bool = bool;
    };

    const clearFlash = () => {
      flash.value.msg = "";
    };

    const setLoggedIn = (data = {}) => {
      loggedIn.value = !loggedIn.value;
      user.value = data;
    };

    const logOut = (val, status) => {
      localStorage.clear();
      router.push({
        name: "LoginPage",
        query: {
          ...route.query,
        },
      });
      setLoggedIn();
      setFlash(val, status);
    };

    const getUser = async () => {
      try {
        const { res, data } = await customFetcher(`user/current`);
        setLoggedIn(data);
      } catch {
        setFlash(err.msg, err.val);
      }
    };

    onBeforeMount(() => {
      setTimeout(showAppFunc, 5000);
      if (localStorage.getItem("ref")) {
        getUser();
      }
    });

    return {
      flash,
      setFlash,
      clearFlash,
      loggedIn,
      setLoggedIn,
      logOut,
      user,
      customFetcher,
      unSecFetcher,
      err,
      showApp,
    };
  },
};
</script>

<style>
::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

::-webkit-scrollbar-track {
  background: #030303;
}

::-webkit-scrollbar-thumb {
  background: rgb(48, 48, 48);
}

::-webkit-scrollbar-thumb:hover {
  background: rgb(105, 105, 105);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
  -webkit-transform: rotateZ(-10deg);
  -ms-transform: rotateZ(10deg);
  transform: rotateZ(-10deg);
  margin-top: 70px;
}

.fade-enter-from {
  opacity: 0;
}

.fade-enter-to {
  opacity: 0;
}

.fade-leave-from {
  opacity: 1;
}

.fade-leave-to {
  opacity: 0;
}
</style>
