import { ref } from "vue";

const upload_preset = "unknown";
const Url = "unknown";

export default function useComp(initialParam = "Composable data") {
  const pic = ref("");
  const ld1 = ref("");
  const ld2 = ref("");
  const covPh = ref("");

  async function getCloudLink(newPic) {
    const formData = new FormData();
    formData.append("upload_preset", upload_preset);
    formData.append("file", newPic);

    let res = await fetch(`${Url}`, { method: "POST", body: formData });
    let data = await res.json();
    let secure_url = await data.secure_url;
    return secure_url;
  }

  async function upImg1(e, val) {
    if (val == 1) {
      pic.value = "";
      ld1.value = "Loading...";
    } else {
      covPh.value = "";
      ld2.value = "Loading...";
    }
    const fileList = e.target.files || e.dataTransfer.files;
    const file = fileList[0];
    if (file) {
      var fileType = file.type;
    }
    if (fileType) {
      var fileGroup = fileType.split("/")[0];
    }
    if (fileGroup !== "image") {
      if (val == 1) {
        ld1.value = "Not an image!";
      } else {
        ld2.value = "Not an image!";
      }
    } else {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = async (e) => {
        try {
          if (val == 1) {
            pic.value = await getCloudLink(e.target.result);
            ld1.value = "";
          } else {
            covPh.value = await getCloudLink(e.target.result);
            ld2.value = "";
          }
        } catch (e) {
          if (val == 1) {
            ld1.value = "Failed!";
          } else {
            ld2.value = "Failed!";
          }
        }
      };
    }
  }

  function cl1() {
    pic.value = "";
  }

  function cl2() {
    covPh.value = "";
  }

  async function upVid(e, setter, run, func) {
    const fileList = e.target.files || e.dataTransfer.files;
    const file = fileList[0];
    if (file) {
      var fileType = file.type;
    }
    if (fileType) {
      var fileGroup = fileType.split("/")[0];
    }
    if (fileGroup !== "video") {
      run("Not a video!");
    } else {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = (e) => {
        getCloudLink(e.target.result, setter, run);
        func(file.name);
      };
    }
  }

  return { upImg1, upVid, getCloudLink, pic, covPh, ld1, ld2, cl1, cl2 };
}
