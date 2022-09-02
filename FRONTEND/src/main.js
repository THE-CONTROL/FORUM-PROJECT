import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./index.css";

import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faAngleLeft,
  faAngleRight,
  faBars,
  faCancel,
  faComment,
  faFaceFrown,
  faNewspaper,
  faSpinner,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(
  faBars,
  faCancel,
  faXmark,
  faSpinner,
  faFaceFrown,
  faAngleLeft,
  faAngleRight,
  faNewspaper,
  faComment
);

const app = createApp(App);

app.use(router);

app.component("fa", FontAwesomeIcon);

app.mount("#app");
