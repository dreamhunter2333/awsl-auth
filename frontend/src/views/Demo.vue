<script setup>
import { NResult, NCard, NButton } from 'naive-ui'
import { onMounted, ref } from "vue";
import { useMessage } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'

import { api } from '../api';
import { useGlobalState } from '../store'

const { jwtSession, appIdSession } = useGlobalState()
const message = useMessage();
const route = useRoute();
const router = useRouter();

const user = ref(null);

const signOut = () => {
    jwtSession.value = null;
    user.value = null;
    router.push('/demo');
}

onMounted(async () => {
    const code = route.query.code;
    if (!code && !jwtSession.value) {
        return;
    }
    if (code) {
        try {
            const { jwt } = await api.fetch("/api/token", {
                method: "POST",
                message: message,
                body: JSON.stringify({
                    app_id: appIdSession.value || "demo",
                    app_secret: "demo_secret",
                    code: code,
                })
            });
            jwtSession.value = jwt;
        } catch (error) {
            message.error(error.message || "登录失败");
            return;
        }
        router.push('/demo');
    }
    try {
        const app_id = appIdSession.value || "demo";
        user.value = await api.fetch(`/api/info?app_id=${app_id}`, {
            message: message,
            headers: {
                'Authorization': `Bearer ${jwtSession.value}`,
                'Content-Type': 'application/json',
            }
        });
    } catch (error) {
        message.error(error.message || "获取用户信息失败");
    }
})
</script>

<template>
    <div class="main">
        <n-card>
            <h2>用户信息</h2>
            <pre v-if="user">{{ JSON.stringify(user, null, 2) }}</pre>
            <p v-else>
                您还没有登录
            </p>
            <n-button @click="router.push('login')" type="primary" block secondary strong>
                返回登录
            </n-button>
            <n-button @click="signOut" v-if="user" type="primary" block secondary strong>
                退出登录
            </n-button>
        </n-card>
    </div>
</template>

<style scoped>
.main {
    display: flex;
    text-align: left;
    place-items: center;
    justify-content: center;
}

.n-card {
    max-width: 600px;
    margin: 20px;
}
</style>
