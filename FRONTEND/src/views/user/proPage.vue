<template>
  <div v-if="ld" class="max-w-screen pt-20">
    <p class="text-3xl text-center" :class="status ? '' : 'text-red-700'">
      <fa :icon="status ? ['fas', 'spinner'] : ['fas', 'face-frown']" />
      {{ status ? "Loading..." : "Failed!" }}
    </p>
  </div>
  <div v-else class="max-w-screen p-2 pb-5 sm:px-5 md:px-20 lg:px-32 relative">
    <img
      :src="user.cover_photo"
      alt="Cover photo"
      class="w-full h-44 sm:h-72 md:h-80 rounded-lg object-cover"
    />
    <div class="w-full py-6">
      <div
        class="w-full sm:justify-start mt-16 sm:mt-0 sm:w-10/12 lg:w-9/12 mx-auto flex flex-row gap-3 justify-center"
      >
        <button
          class="sm:text-6xl text-2xl bg-blue-600 hover:bg-blue-900 px-4 p-1 z-50 sm:hover:text-blue-600 rounded-md mt-1 sm:bg-transparent sm:hover:bg-transparent"
        >
          <router-link :to="`/${user.username}/post/${user.id}`">
            <fa :icon="['fas', 'newspaper']"
          /></router-link>
        </button>
        <button
          class="sm:text-6xl text-2xl bg-blue-600 hover:bg-blue-900 px-4 p-1 z-50 sm:hover:text-blue-600 rounded-md mt-1 sm:bg-transparent sm:hover:bg-transparent"
        >
          <router-link :to="`/${user.username}/comment/${user.id}`">
            <fa :icon="['fas', 'comment']"
          /></router-link>
        </button>
      </div>
    </div>
    <div
      class="w-full absolute left-0 top-32 sm:top-52 md:top-60 flex flex-row justify-center sm:justify-end sm:w-10/12 lg:w-9/12 mx-auto"
    >
      <div class="w-fit h-fit p-0.5 md:p-1 bg-blue-800 rounded-md">
        <img
          :src="user.profile_picture"
          alt="Profile picture"
          class="w-20 h-32 sm:w-40 sm:h-52 object-cover rounded-md border border-black"
        />
      </div>
    </div>
    <div class="w-full border-2 border-blue-800 px-2 py-4 bg-[#141414] sm:mt-6">
      <h3 class="text-lg font-semibold sm:ml-5 text-blue-800">USER DETAILS:</h3>
      <div class="w-full mt-2 flex flex-col gap-4 sm:px-5 md:px-10">
        <p><span class="font-semibold">NAME: </span>{{ user.name }}</p>
        <p><span class="font-semibold">USERNAME: </span>{{ user.username }}</p>
        <p><span class="font-semibold">EMAIL: </span>{{ user.email }}</p>
        <p v-if="user.about">
          <span class="font-semibold">ABOUT: </span>{{ user.about }}
        </p>
        <p><span class="font-semibold">SEX: </span>{{ user.sex }}</p>
        <p v-if="user.pronouns">
          <span class="font-semibold">PRONOUNS: </span>{{ user.pronouns }}
        </p>
        <p>
          <span class="font-semibold">DATE JOINED: </span>{{ user.date_joined }}
        </p>
        <div v-if="loggedIn" class="w-full justify-end flex flex-row gap-3">
          <button class="text-xs bg-blue-700 hover:bg-blue-900 p-1 rounded-md">
            <router-link :to="`/${user.username}/update`">UPDATE</router-link>
          </button>
          <button class="text-xs bg-red-700 hover:bg-red-900 p-1 rounded-md">
            <router-link :to="`/${user.username}/delete`">DELETE</router-link>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onBeforeMount, onUpdated, ref } from "@vue/runtime-core";
import useComp1 from "../../mix/data.js";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "ProfilePage",
  props: {
    setFlash: Function,
    setLoggedIn: Function,
    logOut: Function,
    loggedIn: Boolean,
  },
  setup(props) {
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const user = ref({});
    const ld = ref(true);
    const status = ref(true);

    const getUser = async () => {
      try {
        const { res, data } = await unSecFetcher(`user/${route.params.userId}`);
        user.value = data;
        ld.value = false;
      } catch {
        status.value = false;
        props.setFlash(err.msg, err.val);
      }
    };

    onBeforeMount(() => {
      getUser();
    });

    onUpdated(() => {
      getUser();
    });

    return { unSecFetcher, customFetcher, err, getUser, user, ld, status };
  },
};
</script>

<style></style>
