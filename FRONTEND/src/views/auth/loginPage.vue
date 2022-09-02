<template>
  <div class="px-3 pb-3 sm:pb-10 sm:px-10 pt-2 w-full md:px-16 lg:px-36">
    <div class="w-full bg-[#141414] flex flex-row pb-5 md:pb-0">
      <div
        v-for="(item, index) in sliderImages"
        :key="index"
        class="w-1/2 hidden md:block h-full p-5"
        :class="index == count ? '' : 'md:hidden'"
      >
        <img
          :src="item.src"
          :alt="item.alt"
          class="w-full h-[448px] rounded-lg bg-[#2E2E2E] object-cover"
        />
      </div>
      <div class="w-full md:w-1/2 py-5 px-3 sm:px-10 md:mt-14">
        <h1 class="text-center font-bold text-lg">Log In</h1>
        <form class="w-full p-3 sm:p-5 flex flex-col gap-5 mt-2">
          <div
            v-for="(item, index) in inputs"
            :key="index"
            class="w-full h-full flex flex-col gap-2"
          >
            <label for="profile picture">{{ item.pH }}:</label>
            <input
              :type="item.type"
              :placeholder="item.pH"
              v-model="item.val.value"
              class="w-full h-10 px-3 border-2 rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
            />
          </div>
        </form>
        <div class="w-full px-3 sm:px-5">
          <button
            type="button"
            class="w-full h-11 bg-green-700 text-lg mt-5 rounded-lg hover:bg-green-900 font-bold"
            @click="signIn()"
            :disabled="dis"
          >
            Sign in
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import sl1 from "../../assets/sl1.jpg";
import sl2 from "../../assets/sl2.jpg";
import sl3 from "../../assets/sl3.jpg";
import sl4 from "../../assets/sl4.jpg";
import useComp1 from "../../mix/data.js";
import { onBeforeMount, onBeforeUnmount } from "@vue/runtime-core";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "LoginPage",
  props: {
    setFlash: Function,
    setLoggedIn: Function,
  },
  setup(props) {
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const email = ref("");
    const password = ref("");
    const count = ref(0);
    const int = ref("");
    const dis = ref(false);
    const inputs = [
      { pH: "Email/Username", type: "text", val: email },
      { pH: "Password", type: "password", val: password },
    ];
    const sliderImages = [
      { src: sl1, alt: "Login Image" },
      { src: sl2, alt: "Login Image" },
      { src: sl3, alt: "Login Image" },
      { src: sl4, alt: "Login Image" },
    ];

    const slide = () => {
      if (count.value == sliderImages.length - 1) {
        count.value = 0;
      } else {
        count.value += 1;
      }
    };

    const signIn = async () => {
      dis.value = true;
      const body = {
        email: email.value.trim(),
        password: password.value.trim(),
      };
      try {
        const { res, data } = await unSecFetcher("user/login", {
          method: "POST",
          body: JSON.stringify(body),
        });
        props.setFlash(data.detail, res.ok);
        if (res.ok) {
          localStorage.setItem("acc", data.access_token);
          localStorage.setItem("ref", data.refresh_token);
          props.setLoggedIn(data.user);
          router.push({
            path: `/profile/${data.user.username}/${data.user.id}`,
            query: {
              ...route.query,
            },
          });
        } else {
          dis.value = false;
        }
      } catch {
        props.setFlash(err.msg, err.val);
        dis.value = false;
      }
    };

    onBeforeMount(() => {
      if (!localStorage.getItem("ref")) {
        int.value = setInterval(slide, 1000);
      } else {
        router.push({
          name: "AllPosts",
          query: {
            ...route.query,
          },
        });
        props.setFlash(err.msg1, err.val1);
      }
    });

    onBeforeUnmount(() => {
      clearInterval(int.value);
    });

    return {
      inputs,
      email,
      password,
      sliderImages,
      count,
      int,
      slide,
      signIn,
      unSecFetcher,
      customFetcher,
      err,
      dis,
    };
  },
};
</script>

<style></style>
