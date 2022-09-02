<template>
  <div v-if="ld" class="max-w-screen pt-20">
    <p class="text-3xl text-center" :class="status ? '' : 'text-red-700'">
      <fa :icon="status ? ['fas', 'spinner'] : ['fas', 'face-frown']" />
      {{ status ? "Loading..." : "Failed!" }}
    </p>
  </div>
  <div v-else class="w-full">
    <h2
      class="text-center font-semibold sm:font-bold sm:text-lg md:text-xl mt-2 px-2 overflow-auto"
    >
      <router-link
        :to="`/profile/${username}/${userId}`"
        class="hover:text-blue-800"
      >
        {{ user?.username ? "My" : username + `'s` }}</router-link
      >
      Post(s)
    </h2>
    <div
      v-if="posts?.length"
      class="p-5 w-full flex flex-col gap-4 sm:gap-6 md:gap-8"
    >
      <div
        v-for="(item, index) in posts"
        :key="index"
        class="w-full md:w-10/12 lg:w-8/12 mx-auto rounded-md"
      >
        <div
          class="w-full p-1 sm:p-2 bg-[#101010] hover:bg-[#202020] border-b-2 border-blue-800 rounded-t-md"
        >
          <router-link
            :to="`/profile/${item.username}/${item.user_id}`"
            class="w-full flex flex-row gap-1.5"
          >
            <img
              :src="item.user_pic"
              alt="Username"
              class="w-12 h-12 sm:w-16 sm:h-16 rounded-full object-cover"
            />
            <div class="flex flex-col sm:mt-1 text-left">
              <h3 class="text-sm font-semibold sm:text-xl">
                {{ item.user_name }}
              </h3>
              <h4 class="italic text-sm sm:text-base">{{ item.username }}</h4>
            </div>
          </router-link>
        </div>
        <div
          class="w-full bg-[#303030] hover:bg-[#404040] rounded-b-md px-8 py-4 text-center sm:text-xl text-lg sm:px-12"
        >
          <router-link :to="`/post/content/${item.id}`" class="w-full">
            <h4 class="font-bold">{{ item.heading }}</h4>
            <img
              v-if="item.image"
              :src="item.image"
              alt="Post Image"
              class="w-10/12 mx-auto object-cover h-32 mt-2 sm:h-44 sm:w-96"
            />
            <div class="w-full flex justify-end mt-2">
              <p class="text-xs">Date Added: {{ item.date_created }}</p>
            </div>
          </router-link>
          <div
            v-if="item.user_id == user?.id"
            class="w-full flex flex-row gap-4 justify-center pt-1"
          >
            <router-link
              :to="`/post/update/${item.id}`"
              class="p-1 rounded-md bg-blue-600 hover:bg-blue-800 text-xs mt-2"
              >Update</router-link
            >
            <router-link
              :to="`/post/delete/${item.id}`"
              class="p-1 rounded-md bg-red-600 hover:bg-red-800 text-xs mt-2"
              >Delete</router-link
            >
          </div>
        </div>
      </div>
      <div
        class="max-w-full md:max-w-10/12 lg:max-w-8/12 mx-auto gap-0.5 bg-[#383838] rounded-md overflow-auto flex flex-row"
      >
        <p
          v-if="meta?.prev_page"
          class="p-1 sm:p-2 text-sm bg-[#1d1d1d] hover:bg-[#2c2c2c]"
          @click="getPosts(meta?.prev_page)"
        >
          <fa :icon="['fas', 'angle-left']" />
        </p>
        <p
          v-for="(item, index) in meta?.pages"
          :key="index"
          class="p-0.5 sm:p-1 text-sm hover:bg-[#1d1d1d]"
          @click="getPosts(item)"
          :class="item == meta?.page ? 'bg-[#1d1d1d]' : 'bg-[#2c2c2c]'"
        >
          {{ item }}
        </p>
        <p
          v-if="meta?.next_page"
          class="p-1 sm:p-2 text-sm bg-[#1d1d1d] hover:bg-[#2c2c2c]"
          @click="getPosts(meta?.next_page)"
        >
          <fa :icon="['fas', 'angle-right']" />
        </p>
      </div>
    </div>
    <div v-else>
      <p
        class="pt-2 text-lg font-semibold sm:text-xl sm:pt-4 text-white text-center"
      >
        No posts yet
      </p>
    </div>
  </div>
</template>

<script>
import { onBeforeMount, ref } from "@vue/runtime-core";
import useComp1 from "../../mix/data.js";
import { useRouter, useRoute } from "vue-router";
export default {
  name: "UserPosts",
  props: {
    user: Object,
    setFlash: Function,
  },
  setup(props) {
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const username = route.params.username;
    const userId = route.params.id;
    const posts = ref([]);
    const meta = ref({});
    const ld = ref(true);
    const status = ref(true);

    const getPosts = async (page = 1) => {
      try {
        const { res, data } = await unSecFetcher(
          `user/posts/all/${route.params.id}/${page}`
        );
        posts.value = data.items;
        meta.value = data.meta;
        ld.value = false;
      } catch {
        status.value = false;
        props.setFlash(err.msg, err.val);
      }
    };

    onBeforeMount(() => {
      getPosts();
    });

    return {
      unSecFetcher,
      customFetcher,
      err,
      getPosts,
      posts,
      ld,
      status,
      meta,
      username,
      userId,
    };
  },
};
</script>

<style></style>
