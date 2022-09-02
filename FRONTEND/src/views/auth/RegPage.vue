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
          class="w-full h-[448px] rounded-lg bg-[#2E2E2E]"
        />
      </div>
      <div class="w-full md:w-1/2 py-5 px-3 sm:px-10">
        <h1 class="text-center font-bold text-lg">Register</h1>
        <form
          class="w-full p-3 sm:p-5 flex flex-col gap-5 h-80 mt-2 overflow-auto"
        >
          <div
            v-for="(item, index) in inputs"
            :key="index"
            class="w-full h-full flex flex-col gap-2"
          >
            <label :for="item.pH">{{ item.pH }}:</label>
            <input
              :name="item.pH"
              :type="item.type"
              :placeholder="item.pH"
              v-model="item.val.value"
              class="w-full h-10 px-3 border-2 rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
            />
          </div>
          <div class="w-full h-full flex flex-col gap-2">
            <label for="sex">Sex:</label>
            <select
              name="sex"
              v-model="sex"
              class="w-full h-10 px-3 border-2 rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Non-binary">I don't identify as either</option>
            </select>
          </div>
          <div class="w-full h-full flex flex-col gap-2">
            <label for="profile picture">Profile Picture:</label>
            <input
              type="file"
              class="w-full h-10 px-3 border-2 rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
              name="profile picture"
              @change="upProfPic"
            />
            <div class="w-full">
              <div v-if="pic" class="w-full">
                <div class="mx-auto text-right w-12">
                  <button class="text-red-600 hover:text-red-800" @click="cl1">
                    <fa :icon="['fas', 'xmark']" />
                  </button>
                </div>
                <img
                  :src="pic"
                  alt=""
                  class="h-12 w-12 mx-auto rounded-md object-cover"
                />
              </div>
              <p v-else-if="ld1" class="text-semibold text-center">{{ ld1 }}</p>
            </div>
          </div>
          <div class="w-full h-full flex flex-col gap-2">
            <label for="profile picture">Cover Photo:</label>
            <input
              type="file"
              class="w-full h-10 px-3 border-2 rounded-md bg-[#1b265877] focus:border-0 focus:bg-[#11183877]"
              name="profile picture"
              @change="upCovPh"
            />
            <div class="w-full">
              <div v-if="covPh" class="w-full">
                <div class="mx-auto text-right w-12">
                  <button class="text-red-600 hover:text-red-800" @click="cl2">
                    <fa :icon="['fas', 'xmark']" />
                  </button>
                </div>
                <img
                  :src="covPh"
                  alt=""
                  class="h-12 w-12 mx-auto rounded-md object-cover"
                />
              </div>
              <p v-else-if="ld2" class="text-semibold text-center">{{ ld2 }}</p>
            </div>
          </div>
        </form>
        <div class="w-full px-3 sm:px-5">
          <button
            type="button"
            class="w-full h-11 bg-green-700 text-lg mt-5 rounded-lg hover:bg-green-900 font-bold"
            @click="signUp()"
            :disabled="dis"
          >
            Sign up
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import sl5 from "../../assets/sl5.jpg";
import sl6 from "../../assets/sl6.jpg";
import sl7 from "../../assets/sl7.jpg";
import sl8 from "../../assets/sl8.jpg";
import { onBeforeMount, onBeforeUnmount } from "@vue/runtime-core";
import useComp from "../../mix/media.js";
import useComp1 from "../../mix/data.js";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "RegisterPage",
  props: {
    setFlash: Function,
  },
  setup(props) {
    const { upImg1, upVid, getCloudLink, pic, covPh, ld1, ld2, cl1, cl2 } =
      useComp();
    const { unSecFetcher, customFetcher, err } = useComp1();
    const router = useRouter();
    const route = useRoute();
    const username = ref("");
    const name = ref("");
    const email = ref("");
    const about = ref("");
    const sex = ref("Male");
    const pronouns = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const count = ref(0);
    const dis = ref(false);
    const int = ref("");
    const inputs = [
      { pH: "Name", type: "text", val: name },
      { pH: "Username", type: "text", val: username },
      { pH: "Email", type: "email", val: email },
      { pH: "About", type: "text", val: about },
      { pH: "Pronouns", type: "text", val: pronouns },
      { pH: "Password", type: "password", val: password },
      { pH: "Confirm password", type: "password", val: confirmPassword },
    ];
    const sliderImages = [
      { src: sl5, alt: "Register Image" },
      { src: sl6, alt: "Register Image" },
      { src: sl7, alt: "Register Image" },
      { src: sl8, alt: "Register Image" },
    ];

    const slide = () => {
      if (count.value == sliderImages.length - 1) {
        count.value = 0;
      } else {
        count.value += 1;
      }
    };

    const upProfPic = async (e) => {
      upImg1(e, 1);
    };

    const upCovPh = async (e) => {
      await upImg1(e, 2);
    };

    const signUp = async () => {
      dis.value = true;
      const body = {
        name: name.value.trim(),
        username: username.value.trim(),
        email: email.value.trim(),
        about: about.value.trim(),
        sex: sex.value.trim(),
        pronouns: pronouns.value.trim(),
        profile_picture: pic.value.trim(),
        cover_photo: covPh.value.trim(),
        password: password.value.trim(),
        confirm_password: confirmPassword.value.trim(),
      };
      try {
        const { res, data } = await unSecFetcher("user/register", {
          method: "POST",
          body: JSON.stringify(body),
        });
        props.setFlash(data.detail, res.ok);
        if (res.ok) {
          router.push({
            name: "LoginPage",
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
      username,
      email,
      about,
      sex,
      pronouns,
      password,
      confirmPassword,
      sliderImages,
      count,
      int,
      slide,
      signUp,
      upImg1,
      upVid,
      getCloudLink,
      pic,
      covPh,
      ld1,
      ld2,
      upProfPic,
      upCovPh,
      cl1,
      cl2,
      unSecFetcher,
      customFetcher,
      err,
      dis,
      name,
    };
  },
};
</script>

<style></style>
