import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";

export const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/pages/Home.vue"),
    meta: {
      title: "AI Chat System",
    },
  },
  {
    path: "/ai-settings",
    name: "AISettings",
    component: () => import("@/pages/AISettings.vue"),
    meta: {
      title: "AI Settings",
    },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
