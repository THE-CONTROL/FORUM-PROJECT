<template>
  <div v-if="ld" class="max-w-screen pt-20">
    <p class="text-3xl text-center" :class="status ? '' : 'text-red-700'">
      <fa :icon="status ? ['fas', 'spinner'] : ['fas', 'face-frown']" />
      {{ status ? "Loading..." : "Failed!" }}
    </p>
  </div>
  <div
    v-else
    class="max-w-screen lg:w-9/12 p-3 pb-5 sm:px-5 md:px-16 lg:px-20 mx-auto relative text-center"
  >
    <div
      class="w-full p-1 sm:p-2 bg-[#101010] hover:bg-[#202020] border-b-2 border-blue-800 rounded-t-md"
    >
      <router-link
        :to="`/profile/${post.username}/${post.user_id}`"
        class="w-full flex flex-row gap-1.5"
      >
        <img
          :src="post.user_pic"
          alt="Username"
          class="w-12 h-12 sm:w-16 sm:h-16 rounded-full object-cover"
        />
        <div class="flex flex-col sm:mt-1 text-left">
          <h3 class="font-semibold sm:text-xl">{{ post.user_name }}</h3>
          <h4 class="italic">{{ post.username }}</h4>
        </div>
      </router-link>
    </div>
    <div class="w-fit bg-[#181818] p-2">
      <img
        v-if="post.image"
        :src="post.image"
        alt="Cover photo"
        class="max-w-full rounded-lg object-cover mx-auto"
      />
      <h1
        class="text-2xl sm:text-3xl md:text-4xl font-bold mt-2 sm:mt-4 md:mt-6 text-left"
      >
        {{ post.heading }}
      </h1>
      <div class="w-full max-h-screen overflow-auto mt-2">
        <p
          v-for="(item, index) in text"
          :key="index"
          class="mt-1 sm:mt-2 md:mt-3 text-left"
        >
          {{ item }}
        </p>
      </div>
      <div class="w-full flex justify-end mt-4">
        <p class="text-xs">Date Added: {{ post.date_created }}</p>
      </div>
      <div
        v-if="post.user_id == user?.id"
        class="w-full flex flex-row gap-4 justify-center pb-3"
      >
        <router-link
          :to="`/post/update/${post.id}`"
          class="p-1 rounded-md bg-blue-600 hover:bg-blue-800 text-xs mt-2"
          >Update</router-link
        >
        <router-link
          :to="`/post/delete/${post.id}`"
          class="p-1 rounded-md bg-red-600 hover:bg-red-800 text-xs mt-2"
          >Delete</router-link
        >
      </div>
    </div>
    <div class="w-full mt-5">
      <h2 class="font-semibold text-lg text-left px-2 border-b-2">COMMENTS:</h2>
      <div v-if="post?.comments?.length" class="w-full">
        <div
          v-for="(item, index) in post.comments"
          :key="index"
          class="w-full mt-4"
        >
          <router-link
            :to="`/profile/${item.username}/${item.user_id}`"
            class="w-full"
          >
            <div
              class="w-full bg-[#101010] hover:bg-[#202020] p-1 flex flex-row gap-1.5 border-b-2 border-blue-800"
            >
              <img
                :src="item.user_pic"
                alt="User image"
                class="w-8 h-8 sm:w-12 sm:h-12 rounded-full mt-1 sm:mt-0.5 object-cover"
              />
              <div class="flex flex-col text-left">
                <h3 class="text-sm font-semibold sm:text-xl">
                  {{ item.user_name }}
                </h3>
                <h4 class="italic text-sm sm:text-base">{{ item.username }}</h4>
              </div>
            </div>
          </router-link>
          <div class="w-full bg-[#303030]">
            <p
              class="p-1 px-2 text-sm sm:text-base sm:p-2 overflow-auto max-h-28 text-left"
            >
              {{ item.content }}
            </p>
            <div class="w-full flex justify-end mt-2 px-2 pb-1">
              <p class="text-xs">Date Added: {{ item.date_created }}</p>
            </div>
            <div v-if="item.user_id == user?.id">
              <div
                v-if="!(upVal == item.id)"
                class="w-full flex flex-row gap-4 justify-center pb-3"
              >
                <button
                  class="p-1 rounded-md bg-blue-600 hover:bg-blue-800 text-xs mt-2"
                  @click="setShowUpdate(item.id, item.content)"
                  :disabled="dis1"
                >
                  Update
                </button>
                <button
                  class="p-1 rounded-md bg-red-600 hover:bg-red-800 text-xs mt-2"
                  @click="delComment(item.id)"
                  :disabled="dis2"
                >
                  Delete
                </button>
              </div>
              <div
                v-if="upVal == item.id"
                class="w-full flex flex-col gap-4 justify-center pb-3"
              >
                <textarea
                  type="text"
                  class="w-10/12 h-6 mx-auto px-2 border rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
                  v-model="content"
                  placeholder="Update Comment"
                />
                <div class="w-full flex flex-row gap-2 justify-center">
                  <button
                    class="p-1 rounded-md bg-green-600 hover:bg-green-800 text-xs mt-2"
                    @click="updateComment(item.id)"
                  >
                    Update
                  </button>
                  <button
                    class="p-1 rounded-md bg-red-600 hover:bg-red-800 text-xs mt-2"
                    @click="setShowUpdate()"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
          class="max-w-full w-fit mt-4 md:max-w-10/12 lg:max-w-8/12 mx-auto gap-0.5 bg-[#383838] rounded-md overflow-auto flex flex-row"
        >
          <p
            v-if="meta?.prev_page"
            class="p-0.5 sm:p-1 text-sm bg-[#1d1d1d] hover:bg-[#2c2c2c]"
            @click="getComments(meta?.prev_page)"
          >
            <fa :icon="['fas', 'angle-left']" />
          </p>
          <p
            v-for="(item, index) in meta?.pages"
            :key="index"
            class="p-0.5 sm:p-1 text-sm hover:bg-[#1d1d1d]"
            @click="getComments(item)"
            :class="item == meta?.page ? 'bg-[#1d1d1d]' : 'bg-[#2c2c2c]'"
          >
            {{ item }}
          </p>
          <p
            v-if="meta?.next_page"
            class="p-0.5 sm:p-1 text-sm bg-[#1d1d1d] hover:bg-[#2c2c2c]"
            @click="getComments(meta?.next_page)"
          >
            <fa :icon="['fas', 'angle-right']" />
          </p>
        </div>
      </div>
      <div v-else>
        <p class="pt-2 sm:pt-4 text-center">No comments yet</p>
      </div>
      <div class="w-full mt-5" v-if="!upVal && user?.username">
        <textarea
          type="text"
          class="w-full h-8 px-3 border-2 rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
          v-model="content"
          placeholder="Add Comment"
        />
        <button
          @click="addComment()"
          class="p-1 rounded-md bg-blue-600 hover:bg-blue-800 text-xs mt-2"
          :disabled="dis"
        >
          Add Comment
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { onBeforeMount, ref } from "@vue/runtime-core";
import useComp1 from "../../mix/data.js";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "PostContent",
  props: {
    setFlash: Function,
    setLoggedIn: Function,
    logOut: Function,
    loggedIn: Boolean,
    user: Object,
  },
  setup(props) {
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const post = ref({});
    const meta = ref({});
    const ld = ref(true);
    const status = ref(true);
    const dis = ref(false);
    const dis1 = ref(false);
    const dis2 = ref(false);
    const content = ref("");
    const text = ref([]);
    const upVal = ref(0);

    const getPost = async () => {
      try {
        const { res, data } = await unSecFetcher(`post/${route.params.id}`);
        post.value = data;
        text.value = data.content.split("//");
        getComments();
        ld.value = false;
        window.scroll(0, 0);
      } catch {
        status.value = false;
        props.setFlash(err.msg, err.val);
      }
    };

    const getComments = async (page = 1) => {
      try {
        const { res, data } = await unSecFetcher(
          `post/comments/all/${post.value.id}/${page}`
        );
        post.value.comments = data.items;
        meta.value = data.meta;
        content.value = "";
      } catch {
        props.setFlash(err.msg, err.val);
      }
    };

    const addComment = async () => {
      dis.value = true;
      const body = {
        content: content.value.trim(),
      };
      try {
        const { res, data } = await customFetcher(
          `comment/create/${post.value.id}`,
          { method: "POST", body: JSON.stringify(body) }
        );
        props.setFlash(data.detail, res.ok);
        dis.value = false;
        if (res.ok) {
          getComments();
        }
      } catch {
        props.setFlash(err.msg, err.val);
        dis.value = false;
      }
    };

    const updateComment = async (comId) => {
      dis1.value = true;
      const body = {
        content: content.value.trim(),
      };
      try {
        const { res, data } = await customFetcher(
          `comment/update/${post.value.id}/${comId}`,
          { method: "PUT", body: JSON.stringify(body) }
        );
        props.setFlash(data.detail, res.ok);
        dis1.value = false;
        if (res.ok) {
          getComments();
          setShowUpdate();
        }
      } catch {
        props.setFlash(err.msg, err.val);
        dis1.value = false;
      }
    };

    const delComment = async (comId) => {
      dis2.value = true;
      try {
        const { res, data } = await customFetcher(
          `comment/delete/${post.value.id}/${comId}`,
          { method: "DELETE" }
        );
        props.setFlash(data.detail, res.ok);
        dis2.value = false;
        if (res.ok) {
          getComments();
        }
      } catch {
        props.setFlash(err.msg, err.val);
        dis2.value = false;
      }
    };

    const setShowUpdate = (id = 0, cont = "") => {
      upVal.value = id;
      content.value = cont;
    };

    onBeforeMount(() => {
      getPost();
    });

    return {
      unSecFetcher,
      customFetcher,
      err,
      getPost,
      post,
      ld,
      status,
      addComment,
      dis,
      content,
      upVal,
      setShowUpdate,
      updateComment,
      dis1,
      dis2,
      delComment,
      meta,
      getComments,
      text,
    };
  },
};
</script>

<style></style>
