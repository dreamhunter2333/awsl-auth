<script setup>
import { NGrid, NGi, NSpace, NAlert, NButton, NMessageProvider } from 'naive-ui'
import { NConfigProvider, NBackTop } from 'naive-ui';
import { darkTheme, NGlobalStyle } from 'naive-ui'
import { computed } from "vue";
import { zhCN } from 'naive-ui'
import { useGlobalState } from './store'

import Header from './views/Header.vue';

const { themeSwitch, loading } = useGlobalState()

const theme = computed(() => themeSwitch.value ? darkTheme : null)
</script>

<template>
  <n-config-provider :locale="zhCN" :theme="theme">
    <n-global-style />
    <n-spin description="loading..." :show="loading">
      <n-message-provider>
        <div class="main">
          <Header />
          <router-view></router-view>
        </div>
      </n-message-provider>
    </n-spin>
    <n-back-top />
  </n-config-provider>
</template>

<style scoped>
.main {
  text-align: center;
  justify-content: center;
}
</style>

<style>
.n-button {
  text-align: center;
  margin-bottom: 12px;
}
</style>
