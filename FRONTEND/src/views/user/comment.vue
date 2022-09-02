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
      Comment(s)
    </h2>
    <div
      v-if="comments?.length"
      class="p-5 w-full flex flex-col gap-4 sm:gap-6 md:gap-8"
    >
      <div
        v-for="(item, index) in comments"
        :key="index"
        class="w-full md:w-10/12 lg:w-8/12 mx-auto rounded-md"
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
              class="w-8 h-8 sm:w-12 sm:h-12 rounded-full object-cover"
            />
            <div class="flex flex-col text-left">
              <h3 class="text-sm font-semibold sm:text-xl">
                {{ item.user_name }}
              </h3>
              <h4 class="italic text-sm sm:text-base">{{ item.username }}</h4>
            </div>
          </div>
        </router-link>
        <div class="w-full bg-[#303030] hover:bg-[#404040] text-center">
          <router-link :to="`/post/content/${item.post_id}`" class="w-full">
            <p
              class="p-1 px-2 text-sm sm:text-base sm:p-2 overflow-auto max-h-28 text-left"
            >
              {{ item.content }}
            </p>
            <div class="w-full flex justify-end mt-2 px-2 pb-1">
              <p class="text-xs">Date Added: {{ item.date_created }}</p>
            </div>
          </router-link>
          <div v-if="item.user_id == user?.id" class="mt-2">
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
                  @click="updateComment(item.id, item.post_id)"
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
  </div>
</template>

<script>
import { onBeforeMount, ref } from "@vue/runtime-core";
import useComp1 from "../../mix/data.js";
import { useRouter, useRoute } from "vue-router";
export default {
  name: "UserComments",
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
    const comments = ref([]);
    const meta = ref({});
    const ld = ref(true);
    const status = ref(true);
    const dis1 = ref(false);
    const dis2 = ref(false);
    const content = ref("");
    const upVal = ref(0);

    const getComments = async (page = 1) => {
      try {
        const { res, data } = await unSecFetcher(
          `user/comments/all/${route.params.id}/${page}`
        );
        comments.value = data.items;
        meta.value = data.meta;
        ld.value = false;
      } catch {
        status.value = false;
        props.setFlash(err.msg, err.val);
      }
    };

    const updateComment = async (comId, postId) => {
      dis1.value = true;
      const body = {
        content: content.value.trim(),
      };
      try {
        const { res, data } = await customFetcher(
          `comment/update/${postId}/${comId}`,
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
          `comment/delete/${comment.value.id}/${comId}`,
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
      getComments();
    });

    return {
      unSecFetcher,
      customFetcher,
      err,
      getComments,
      comments,
      ld,
      status,
      meta,
      username,
      setShowUpdate,
      delComment,
      delComment,
      updateComment,
      dis1,
      dis2,
      upVal,
      content,
      userId,
    };
  },
};
</script>

<style></style>
