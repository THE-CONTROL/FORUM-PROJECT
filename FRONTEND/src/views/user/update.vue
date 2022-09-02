<template>
  <div v-if="ld" class="max-w-screen pt-20">
    <p class="text-3xl text-center" :class="status ? '' : 'text-red-700'">
      <fa :icon="status ? ['fas', 'spinner'] : ['fas', 'face-frown']" />
      {{ status ? "Loading..." : "Failed!" }}
    </p>
  </div>
  <div v-else class="max-w-screen p-2 pb-5 sm:px-5 md:px-20 lg:px-32 relative">
    <div
      class="w-full mx-auto md:w-1/2 bg-[#141414] flex flex-row pb-5 md:pb-0"
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
                <div class="w-8 mx-auto text-right sm:w-12">
                  <button class="text-red-600 hover:text-red-800" @click="cl2">
                    <fa :icon="['fas', 'xmark']" />
                  </button>
                </div>
                <img
                  :src="covPh"
                  alt=""
                  class="h-8 w-8 sm:h-12 sm:w-12 mx-auto rounded-md object-cover"
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
            @click="update()"
            :disabled="dis"
          >
            Update
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
  name: "UpdatePage",
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
    const username = ref("");
    const name = ref("");
    const email = ref("");
    const about = ref("");
    const sex = ref("Male");
    const pronouns = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const dis = ref(false);
    const ld = ref(true);
    const status = ref(true);
    const inputs = [
      { pH: "Name", type: "text", val: name },
      { pH: "Username", type: "text", val: username },
      { pH: "Email", type: "email", val: email },
      { pH: "About", type: "text", val: about },
      { pH: "Pronouns", type: "text", val: pronouns },
    ];

    const getUser = async () => {
      try {
        const { res, data } = await customFetcher("user/current");
        name.value = data.name;
        username.value = data.username;
        email.value = data.email;
        about.value = data.about;
        sex.value = data.sex;
        pronouns.value = data.pronouns;
        pic.value = data.profile_picture;
        covPh.value = data.cover_photo;
        ld.value = false;
      } catch {
        status.value = false;
        props.setFlash(err.msg, err.val);
      }
    };

    const upProfPic = async (e) => {
      upImg1(e, 1);
    };

    const upCovPh = async (e) => {
      upImg1(e, 2);
    };

    const update = async () => {
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
      };
      try {
        const { res, data } = await customFetcher("user/update", {
          method: "PUT",
          body: JSON.stringify(body),
        });
        props.setFlash(data.detail, res.ok);
        if (res.ok) {
          props.logOut(data.detail, res.ok);
        } else {
          dis.value = false;
        }
      } catch {
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

    return {
      inputs,
      username,
      email,
      about,
      sex,
      pronouns,
      password,
      confirmPassword,
      update,
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
      ld,
      status,
      name,
    };
  },
};
</script>

<style></style>
