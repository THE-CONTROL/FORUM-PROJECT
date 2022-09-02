<template>
  <div v-if="ld" class="max-w-screen pt-20">
    <p class="text-3xl text-center" :class="status ? '' : 'text-red-700'">
      <fa :icon="status ? ['fas', 'spinner'] : ['fas', 'face-frown']" />
      {{ status ? "Loading..." : "Failed!" }}
    </p>
  </div>
  <div v-else class="px-3 pb-3 sm:pb-10 sm:px-10 pt-2 w-full h-full">
    <div
      class="w-full mx-auto md:w-1/2 bg-[#141414] flex flex-row pb-5 md:pb-0"
    >
      <div class="w-full py-5 px-3 sm:px-10">
        <h1 class="text-center font-bold text-lg">Delete Your Account</h1>
        <div class="w-full p-3 sm:p-5 flex flex-col gap-5 mt-2">
          <div class="w-full text-center">
            <p>
              Deleting your account will result in loss of all associated data.
            </p>
            <p class="text-red-600">
              Are you sure you want to delete your account?
            </p>
          </div>
          <div class="w-full text-center">
            <img
              :src="user.profile_picture"
              :alt="user.username"
              class="w-24 h-24 sm:w-32 sm:h-32 md:w-40 md:h-40 rounded-full mx-auto mb-2 object-cover"
            />
            <h3 class="w-full text-lg font-semibold overflow-auto">
              {{ user.name }}
            </h3>
            <p class="w-full overflow-auto">{{ user.username }}</p>
          </div>
        </div>
        <div class="w-full px-5 flex flex-row gap-2 justify-center">
          <button
            type="button"
            class="bg-red-700 text-xs rounded-md px-3 py-1 hover:bg-red-900"
            @click="del()"
            :disabled="dis"
          >
            Yes
          </button>
          <button
            type="button"
            class="bg-blue-700 text-xs rounded-md px-3 py-1 hover:bg-blue-900"
            :disabled="dis"
          >
            <router-link :to="`/profile/${user.username}/${user.id}`">
              No</router-link
            >
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { onBeforeMount } from "@vue/runtime-core";
import useComp1 from "../../mix/data.js";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "DeletePage",
  props: {
    setFlash: Function,
    setLoggedIn: Function,
    logOut: Function,
  },
  setup(props) {
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const user = ref({});
    const ld = ref(true);
    const status = ref(true);
    const dis = ref(false);

    const getUser = async () => {
      try {
        const { res, data } = await customFetcher("user/current");
        user.value = data;
        ld.value = false;
      } catch {
        status.value = false;
        props.setFlash(err.msg, err.val);
      }
    };

    const del = async () => {
      dis.value = true;
      try {
        const { res, data } = await customFetcher("user/delete", {
          method: "DELETE",
        });
        props.setFlash(data.detail, res.ok);
        if (res.ok) {
          props.logOut(data.detail, res.ok);
        } else {
          dis.value = false;
        }
      } catch (e) {
        props.setFlash(err.msg, err.val);
        dis.value = false;
      }
    };

    onBeforeMount(() => {
      if (localStorage.getItem("ref")) {
        getUser();
      } else {
        router.push({
          name: "LoginPage",
          query: {
            ...route.query,
          },
        });
        props.setFlash(err.msg2, err.val);
      }
    });

    return { user, del, unSecFetcher, customFetcher, err, dis, ld, status };
  },
};
</script>

<style></style>
