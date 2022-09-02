import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "../extras/landingPage.vue";
import RegPage from "../views/auth/RegPage.vue";
import LoginPage from "../views/auth/loginPage.vue";
import ProfilePage from "../views/user/proPage.vue";
import UpdatePage from "../views/user/update.vue";
import DeletePage from "../views/user/del.vue";
import AllPosts from "../views/posts/all.vue";
import CreatePost from "../views/posts/create.vue";
import PostContent from "../views/posts/content.vue";
import UpdatePost from "../views/posts/update.vue";
import DeletePost from "../views/posts/del.vue";
import UserPosts from "../views/user/post.vue";
import UserComments from "../views/user/comment.vue";
import ErrorPage from "../extras/Error.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "LandingPage",
      component: LandingPage,
    },
    {
      path: "/register",
      name: "RegisterPage",
      component: RegPage,
    },
    {
      path: "/login",
      name: "LoginPage",
      component: LoginPage,
    },
    {
      path: "/profile/:username/:userId",
      name: "ProfilePage",
      component: ProfilePage,
    },
    {
      path: "/:user/update",
      name: "UpdatePage",
      component: UpdatePage,
    },
    {
      path: "/:user/delete",
      name: "DeletePage",
      component: DeletePage,
    },
    {
      path: "/posts",
      name: "AllPosts",
      component: AllPosts,
    },
    {
      path: "/posts/create",
      name: "CreatePost",
      component: CreatePost,
    },
    {
      path: "/post/content/:id",
      name: "PostContent",
      component: PostContent,
    },
    {
      path: "/post/update/:id",
      name: "UpdatePost",
      component: UpdatePost,
    },
    {
      path: "/post/delete/:id",
      name: "DeletePost",
      component: DeletePost,
    },
    {
      path: "/:username/post/:id",
      name: "UserPosts",
      component: UserPosts,
    },
    {
      path: "/:username/comment/:id",
      name: "UserComments",
      component: UserComments,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "ErrorPage",
      component: ErrorPage,
    },
  ],
});

export default router;
