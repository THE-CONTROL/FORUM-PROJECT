<template>
  <div class="w-full">
    <div
      class="max-w-screen flex flex-row justify-between py-4 md:py-6 px-5 md:px-10 lg:px-16 border-b sm:border-b-2 border-[#1b1b1b]"
    >
      <router-link
        v-if="loggedIn"
        class="w-fit"
        :to="`/profile/${user.username}/${user.id}`"
        :class="
          route.path == `/profile/${user.username}/${user.id}`
            ? 'text-blue-900'
            : ''
        "
      >
        <div
          class="w-fit flex justify-end font-bold text-sm md:text-lg text-center lg:pt-1.5 hover:text-blue-900 md:mt-3 lg:mt-2"
        >
          <img
            :src="user.profile_picture"
            :class="
              route.path == `/profile/${user.username}/${user.id}`
                ? 'border-2 border-blue-900'
                : ''
            "
            class="h-8 w-8 md:mr-2 float-left rounded-full object-cover"
            :alt="user.username"
          />
          <span class="hidden md:block">{{ user.username }}</span>
        </div>
      </router-link>
      <div
        v-else
        class="w-fit flex justify-end font-bold text-sm md:text-lg text-center lg:pt-1.5 md:mt-3 lg:mt-2"
      >
        <img
          src="https://res.cloudinary.com/de49puo0s/image/upload/v1661298810/s1xpcx5i4xlexkgnmfuw.jpg"
          class="h-8 w-8 md:mr-2 float-left rounded-full object-cover"
          alt="Logo"
        />
        <span class="hidden md:block">CONTROL</span>
      </div>
      <div
        class="w-fit flex justify-end text-center text-xl sm:text-2xl md:text-3xl lg:text-4xl font-bold text-[#3342ce] md:pt-2 lg:pt-1.5"
      >
        <div class="h-8 w-8 md:mr-2 float-left lg:mt-2 md:h-7 md:w-7 md:mt-1">
          <img
            class="w-full h-full md:rounded-lg rounded-md object-cover"
            src="../assets/poseidon.jpg"
            alt="Logo"
          />
        </div>
        <span class="hidden md:block">POSEIDON</span>
      </div>
      <div
        v-if="!loggedIn"
        class="md:flex flex-row gap-4 text-lg pt-0.5 hidden mt-2.5"
      >
        <router-link
          v-for="(li, id) in links"
          :key="id"
          :to="li.to"
          class="hover:text-blue-900 lg:text-lg"
          :class="route.path == li.to ? 'text-blue-900' : ''"
        >
          {{ li.name }}</router-link
        >
      </div>
      <div v-else class="md:flex flex-row gap-4 text-lg pt-0.5 hidden mt-2.5">
        <router-link
          v-for="(li, id) in lgLinks"
          :key="id"
          :to="li.to"
          class="hover:text-blue-900 lg:text-lg"
          :class="route.path == li.to ? 'text-blue-900' : ''"
        >
          {{ li.name }}</router-link
        >
        <span @click="logOut()" class="hover:text-blue-900 lg:text-lg">
          Log Out</span
        >
      </div>
      <div class="text-2xl md:hidden hover:text-gray-400" @click="togNav()">
        <fa :icon="['fas', 'bars']" />
      </div>
    </div>
    <div v-if="showNav" class="w-screen">
      <div
        v-if="!loggedIn"
        class="w-full bg-[#070707] md:hidden flex flex-col text-center gap-2 py-2"
      >
        <router-link
          v-for="(li, id) in links"
          :key="id"
          :to="li.to"
          @click="togNav()"
          :class="route.path == li.to ? 'text-blue-900' : ''"
          class="hover:text-blue-900 lg:text-lg"
          >{{ li.name }}</router-link
        >
      </div>
      <div
        v-else
        class="w-full bg-[#070707] md:hidden flex flex-col text-center gap-2 py-2"
      >
        <router-link
          v-for="(li, id) in lgLinks"
          :key="id"
          :to="li.to"
          @click="togNav()"
          :class="route.path == li.to ? 'text-blue-900' : ''"
          class="hover:text-blue-900 lg:text-lg"
          >{{ li.name }}</router-link
        >
        <span @click="logOut()" class="hover:text-blue-900 lg:text-lg">
          Log Out</span
        >
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { useRoute } from "vue-router";

export default {
  name: "NavBar",
  props: {
    loggedIn: Boolean,
    setFlash: Function,
    setLoggedIn: Function,
    logOut: Function,
    user: Object,
  },
  setup(props) {
    const route = useRoute();
    const links = [
      { name: "All Posts", to: "/posts" },
      { name: "Login", to: "/login" },
      { name: "Register", to: "/register" },
    ];
    const lgLinks = [
      { name: "All Posts", to: "/posts" },
      { name: "Create", to: "/posts/create" },
    ];
    const showNav = ref(false);

    const togNav = () => {
      showNav.value = !showNav.value;
    };

    const logOut = () => {
      togNav();
      props.logOut("Log out successful!", true);
    };

    return { links, togNav, showNav, route, lgLinks, logOut };
  },
};
</script>

<style></style>
