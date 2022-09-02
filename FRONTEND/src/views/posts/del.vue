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
        <h1 class="text-center font-bold text-lg">Delete Post</h1>
        <div class="w-full p-3 sm:p-5 flex flex-col gap-5 mt-2">
          <div class="w-full text-center">
            <p class="text-red-600">
              Are you sure you want to delete this post?
            </p>
          </div>
          <div class="w-full text-center">
            <img
              v-if="post.image"
              :src="post.image"
              :alt="post.heading"
              class="w-28 h-28 sm:w-36 sm:h-36 md:w-44 md:h-44 mx-auto mb-2 object-cover"
            />
            <p class="text-semibold text-lg sm:text-xl md:text-2xl">
              {{ post.heading }}
            </p>
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
            <router-link :to="`/post/content/${post.id}`"> No</router-link>
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
  name: "DeletePost",
  props: {
    setFlash: Function,
    setLoggedIn: Function,
    logOut: Function,
  },
  setup(props) {
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const post = ref({});
    const ld = ref(true);
    const status = ref(true);
    const dis = ref(false);

    const getPost = async () => {
      try {
        const { res, data } = await unSecFetcher(`post/${route.params.id}`);
        post.value = data;
        ld.value = false;
      } catch {
        status.value = false;
        props.setFlash(err.msg, err.val);
      }
    };

    const del = async () => {
      dis.value = true;
      try {
        const { res, data } = await customFetcher(
          `post/delete/${post.value.id}`,
          { method: "DELETE" }
        );
        props.setFlash(data.detail, res.ok);
        if (res.ok) {
          router.push({
            name: "AllPosts",
            query: {
              ...route.query,
            },
          });
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
        getPost();
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

    return { post, del, unSecFetcher, customFetcher, err, dis, ld, status };
  },
};
</script>

<style></style>
