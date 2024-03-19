<script setup>
import { NResult, NCard, NButton } from 'naive-ui'
import { onMounted, ref, computed } from "vue";
import { useMessage } from 'naive-ui'
import { useRouter, useRoute } from 'vue-router'

import { api } from '../api';
import { useGlobalState } from '../store'

const { appIdSession } = useGlobalState()
const message = useMessage();
const router = useRouter();
const route = useRoute();

const isFailed = ref(false);

const title = computed(() => isFailed.value ? "登录失败" : "正在登录中");
const status = computed(() => isFailed.value ? "error" : "success");


onMounted(async () => {
    const reqBody = {
        app_id: appIdSession.value || "demo",
    };
    if (route.path == "/callback/github") {
        reqBody.login_type = "github";
        reqBody.code = route.query.code;
    } else if (route.path == "/callback/google") {
        reqBody.login_type = "google";
        reqBody.code = route.query.code;
        reqBody.redirect_url = window.location.origin + "/callback/google";
    } else if (route.path == "/callback/web3") {
        reqBody.login_type = "web3";
        reqBody.web3_account = route.query.web3_account;
    } else if (route.path == "/callback/ms") {
        reqBody.login_type = "ms";
        reqBody.code = route.query.code;
        reqBody.redirect_url = window.location.origin + "/callback/ms";
    } else {
        isFailed.value = true;
        message.error(`登录失败 ${route.path}`);
        return;
    }
    try {
        const response = await api.fetch(`/api/oauth`, {
            method: "POST",
            body: JSON.stringify(reqBody)
        });
        if (!response) {
            isFailed.value = true;
            message.error(`登录失败 ${response}`);
            return;
        }
        const { code, redirect_url } = response;
        if (!code) {
            isFailed.value = true;
            message.error(`登录失败 ${response}`);
            return;
        }
        if (redirect_url) {
            const url = new URL(redirect_url);
            url.searchParams.set("code", code);
            window.location.href = url.href;
            return;
        }
        router.push(`/demo?code=${code}`);
    } catch (error) {
        isFailed.value = true;
        message.error(`登录失败 ${error.message}`);
        return;
    }
})
</script>

<template>
    <div class="main">
        <n-card>
            <n-result :status="status" :title="title">
                <template #footer v-if="isFailed">
                    <n-button @click="router.push('/')" type="primary" block secondary strong>
                        返回登录
                    </n-button>
                </template>
            </n-result>
        </n-card>
    </div>
</template>

<style scoped>
.main {
    display: flex;
    text-align: center;
    place-items: center;
    justify-content: center;
}

.n-card {
    max-width: 300px;
    margin: 20px;
}
</style>
