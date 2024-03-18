<script setup>
import { NCard, NButton, NTabs, NIcon, NResult } from 'naive-ui'
import { NTabPane, NForm, NFormItem, NFormItemRow, NInput } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { Github, Google } from '@vicons/fa'
import { useRoute } from 'vue-router'

import { onMounted } from "vue";

import { api } from '../api';
import { useGlobalState } from '../store'

const { settings, appIdSession } = useGlobalState()
const message = useMessage();
const route = useRoute();

const onLogin = async (login_type) => {
    try {
        const response = await api.fetch(
            `/api/login?login_type=${login_type}` +
            `&redirect_url=${window.location.origin}/callback/${login_type}`,
            {
                message: message
            }
        );
        if (!response) {
            message.error(`跳转失败 ${response}`);
            return;
        }
        window.location.href = response;
    } catch (error) {
        message.error(error.message || "登录失败");
    }
};

onMounted(async () => {
    appIdSession.value = route.query.app_id;
    try {
        const res = await api.fetch(`/api/settings`, {
            message: message
        });
        settings.value = res;
    } catch (error) {
        message.error(error.message || "获取设置失败");
    }
});
</script>

<template>
    <div class="main">
        <n-card style="max-width: 500px;">
            <img style="max-height: 100px; max-width: auto;" src="/awsl.png">
            <n-tabs default-value="signin" size="large" justify-content="space-evenly">
                <n-tab-pane name="signin" tab="登录">
                    <n-form v-if="settings.enabled_smtp">
                        <n-form-item-row label="邮箱">
                            <n-input />
                        </n-form-item-row>
                        <n-form-item-row label="密码">
                            <n-input type="password" show-password-on="click" />
                        </n-form-item-row>
                        <n-button quaternary size="small">
                            忘记密码?
                        </n-button>
                        <n-button type="primary" block secondary strong>
                            登录
                        </n-button>
                    </n-form>
                    <n-button v-if="settings.enabled_github" block @click="onLogin('github')">
                        <template #icon>
                            <n-icon :component="Github" />
                        </template>
                        Github 登录
                    </n-button>
                    <n-button v-if="settings.enabled_google" block @click="onLogin('google')">
                        <template #icon>
                            <n-icon :component="Google" />
                        </template>
                        Google 登录
                    </n-button>
                </n-tab-pane>
                <n-tab-pane v-if="settings.enabled_smtp" name="signup" tab="注册">
                    <n-form>
                        <n-form-item-row label="邮箱">
                            <n-input />
                        </n-form-item-row>
                        <n-form-item-row label="密码">
                            <n-input type="password" show-password-on="click" />
                        </n-form-item-row>
                        <n-form-item-row label="验证码">
                            <n-input />
                        </n-form-item-row>
                    </n-form>
                    <n-button type="primary" block secondary strong>
                        注册
                    </n-button>
                </n-tab-pane>
            </n-tabs>
        </n-card>
    </div>
</template>

<style scoped>
.main {
    display: flex;
    text-align: center;
    place-items: center;
    justify-content: center;
    margin: 20px;
}
</style>
