<template>
  <div class="px-3 pb-3 sm:pb-10 sm:px-10 pt-2 w-full h-full">
    <div
      class="w-full mx-auto md:w-10/12 lg:w-8/12 bg-[#141414] flex flex-row pb-5 md:pb-0"
    >
      <div class="w-full py-5 px-3 sm:px-10">
        <h1 class="text-center font-bold text-lg">Update Your Profile</h1>
        <form
          class="w-full p-3 sm:p-5 flex flex-col gap-5 h-80 mt-2 overflow-auto"
        >
          <div
            v-for="(item, index) in inputs"
            :key="index"
            class="w-full h-full flex flex-col gap-2"
          >
            <label :for="item.pH">{{ item.pH }}:</label>
            <textarea
              :name="item.pH"
              :placeholder="
                index == 0
                  ? item.pH
                  : `${item.pH} - Use '//' to indicate new paragraph`
              "
              v-model="item.val.value"
              class="w-full px-3 py-1 border-2 rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
              :class="index == 0 ? 'h-10' : 'h-20 sm:h-32 md:h-40'"
            />
          </div>
          <div class="w-full h-full flex flex-col gap-2">
            <label for="image">Image:</label>
            <input
              type="file"
              class="w-full h-10 px-3 border-2 rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
              name="image"
              @change="upProfPic"
            />
            <div class="w-full">
              <div v-if="pic" class="w-full">
                <div class="w-8 mx-auto text-right sm:w-12">
                  <button class="text-red-600 hover:text-red-800" @click="cl1">
                    <fa :icon="['fas', 'xmark']" />
                  </button>
                </div>
                <img
                  :src="pic"
                  alt=""
                  class="h-8 w-8 sm:h-12 sm:w-12 mx-auto rounded-md object-cover"
                />
              </div>
              <p v-else-if="ld1" class="text-semibold text-center">{{ ld1 }}</p>
            </div>
          </div>
        </form>
        <div class="w-full px-3 sm:px-5">
          <button
            type="button"
            class="w-full h-11 bg-green-700 text-lg mt-5 rounded-lg hover:bg-green-900 font-bold"
            @click="create()"
            :disabled="dis"
          >
            Create
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { onBeforeMount } from "@vue/runtime-core";
import useComp from "../../mix/media.js";
import useComp1 from "../../mix/data.js";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "CreatePost",
  props: {
    setFlash: Function,
    setLoggedIn: Function,
    logOut: Function,
  },
  setup(props) {
    const { upImg1, upVid, getCloudLink, pic, covPh, ld1, ld2, cl1, cl2 } =
      useComp();
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const heading = ref("");
    const content = ref("");
    const dis = ref(false);
    const inputs = [
      { pH: "Heading", val: heading },
      { pH: "Content", val: content },
    ];

    const upProfPic = async (e) => {
      upImg1(e, 1);
    };

    const create = async () => {
      dis.value = true;
      const body = {
        heading: heading.value.trim(),
        content: content.value.trim(),
        image: pic.value.trim(),
      };
      try {
        const { res, data } = await customFetcher("post/create", {
          method: "POST",
          body: JSON.stringify(body),
        });
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
        console.log(e);
      }
    };

    onBeforeMount(() => {
      if (!localStorage.getItem("ref")) {
        router.push({
          name: "LoginPage",
          query: {
            ...route.query,
          },
        });
        props.setFlash(err.msg2, err.val);
      }
    });

    return {
      heading,
      content,
      create,
      upImg1,
      upVid,
      getCloudLink,
      pic,
      covPh,
      ld1,
      upProfPic,
      cl1,
      unSecFetcher,
      customFetcher,
      err,
      dis,
      inputs,
    };
  },
};
</script>

<style></style>
