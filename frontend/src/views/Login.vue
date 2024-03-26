<script setup>
import { NCard, NButton, NTabs, NIcon, NResult, NInputGroup } from 'naive-ui'
import { NTabPane, NForm, NFormItem, NFormItemRow, NInput, NModal } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { Github, Google, Microsoft } from '@vicons/fa'
import { useRoute, useRouter } from 'vue-router'

import { computed, onMounted, ref, watch } from "vue";

import { api } from '../api';
import { useGlobalState } from '../store'

const { settings, appIdSession, themeSwitch } = useGlobalState()
const message = useMessage();
const route = useRoute();
const router = useRouter();

const tabValue = ref("tabValue");
tabValue.value = "signin";
const showModal = ref(false);
const user = ref({
    email: "",
    password: "",
    code: ""
});


const isEnableWeb3 = computed(() => {
    return settings.value.enabled_web3 && window.ethereum;
});

const onOauthLogin = async (login_type) => {
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

const web3Login = async () => {
    if (!window.ethereum) return;
    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
    if (accounts.length <= 0) {
        message.error("请安装 MetaMask");
        return;
    }
    const account = accounts[0];
    router.push(`/callback/web3?web3_account=${account}`);
}

const hashPassword = async (password) => {
    // user crypto to hash password
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password));
    const hashArray = Array.from(new Uint8Array(digest));
    return hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
}

const emailLogin = async () => {
    if (!user.value.email || !user.value.password) {
        message.error("请输入邮箱和密码");
        return;
    }
    try {
        const res = await api.fetch(`/api/email/login`, {
            method: "POST",
            body: JSON.stringify({
                email: user.value.email,
                // hash password
                password: await hashPassword(user.value.password)
            }),
            message: message
        });
        if (!res || !res.code) {
            message.error("登录失败");
            return;
        }
        router.push(`/callback/email?code=${res.code}`);
    } catch (error) {
        message.error(error.message || "登录失败");
    }
};

const verify_code_timeout = ref(0);
const sendVerificationCode = async () => {
    if (!user.value.email) {
        message.error("请输入邮箱");
        return;
    }
    if (!cf_token.value && settings.value.cf_turnstile_site_key) {
        message.error("请完成人机验证");
        return;
    }
    try {
        const res = await api.fetch(`/api/email/verify_code`, {
            method: "POST",
            body: JSON.stringify({
                email: user.value.email,
                cf_token: cf_token.value
            }),
            message: message
        });
        if (res && res.timeout) {
            message.success(`验证码已发送, 有效期 ${res.timeout} 秒`);
            verify_code_timeout.value = res.timeout;
            const intervalId = setInterval(() => {
                verify_code_timeout.value -= 1;
                if (verify_code_timeout.value <= 0) {
                    clearInterval(intervalId);
                    verify_code_timeout.value = 0;
                }
            }, 1000);
        }
    } catch (error) {
        message.error(error.message || "发送验证码失败");
    }
};

const emailSignup = async () => {
    if (!user.value.email || !user.value.password || !user.value.code) {
        message.error("请输入邮箱, 密码和验证码");
        return;
    }
    try {
        const res = await api.fetch(`/api/email/register`, {
            method: "POST",
            body: JSON.stringify({
                email: user.value.email,
                // hash password
                password: await hashPassword(user.value.password),
                code: user.value.code
            }),
            message: message
        });
        if (res) {
            tabValue.value = "signin";
            message.success("注册成功, 请登录");
        }
    } catch (error) {
        message.error(error.message || "注册失败");
    }
};

const cf_turnstile_id = ref("")
const cf_token = ref("")
const checkCfTurnstile = async (remove) => {
    if (!settings.value.cf_turnstile_site_key) return;
    let container = document.getElementById("cf-turnstile");
    let count = 100;
    while (!container && count-- > 0) {
        container = document.getElementById("cf-turnstile");
        await new Promise(r => setTimeout(r, 100));
    }
    if (remove && cf_turnstile_id.value) {
        window.turnstile.remove(cf_turnstile_id.value);
    }
    cf_turnstile_id.value = window.turnstile.render(
        "#cf-turnstile",
        {
            sitekey: settings.value.cf_turnstile_site_key,
            language: 'zh-CN',
            theme: themeSwitch.value ? 'dark' : 'light',
            callback: function (token) {
                cf_token.value = token;
            },
        }
    );
}

watch([tabValue, themeSwitch, showModal], async ([newValue, oldValue], [newTheme, oldTheme]) => {
    checkCfTurnstile(newValue != "signup")
}, { immediate: true })

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
            <img style="max-height: 50px; max-width: auto;" src="/awsl.png">
            <n-tabs v-model:value="tabValue" default-value="signin" size="large" justify-content="space-evenly">
                <n-tab-pane name="signin" tab="登录">
                    <n-form v-if="settings.enabled_smtp">
                        <n-form-item-row label="邮箱" required>
                            <n-input v-model:value="user.email" />
                        </n-form-item-row>
                        <n-form-item-row label="密码" required>
                            <n-input v-model:value="user.password" type="password" show-password-on="click" />
                        </n-form-item-row>
                        <n-button @click="emailLogin" type="primary" block secondary strong>
                            登录
                        </n-button>
                        <n-button @click="showModal = true" type="info" quaternary size="tiny">
                            忘记密码?
                        </n-button>
                    </n-form>
                    <n-button v-if="settings.enabled_github" block @click="onOauthLogin('github')">
                        <template #icon>
                            <n-icon :component="Github" />
                        </template>
                        Github 登录
                    </n-button>
                    <n-button v-if="settings.enabled_google" block @click="onOauthLogin('google')">
                        <template #icon>
                            <n-icon :component="Google" />
                        </template>
                        Google 登录
                    </n-button>
                    <n-button v-if="settings.enabled_ms" block @click="onOauthLogin('ms')">
                        <template #icon>
                            <n-icon :component="Microsoft" />
                        </template>
                        Microsoft 登录
                    </n-button>
                    <n-button v-if="isEnableWeb3" block @click="web3Login">
                        <template #icon>
                            <img src="https://metamask.io/images/metamask-logo.png"
                                style="height: 20px; width: auto;" />
                        </template>
                        MetaMask 登录
                    </n-button>
                </n-tab-pane>
                <n-tab-pane v-if="settings.enabled_smtp" name="signup" tab="注册">
                    <n-form>
                        <n-form-item-row label="邮箱" required>
                            <n-input v-model:value="user.email" />
                        </n-form-item-row>
                        <n-form-item-row label="密码" required>
                            <n-input v-model:value="user.password" type="password" show-password-on="click" />
                        </n-form-item-row>
                        <div v-if="settings.cf_turnstile_site_key && !cf_turnstile_id">人机验证正在加载...</div>
                        <div v-if="settings.cf_turnstile_site_key" id="cf-turnstile"></div>
                        <n-form-item-row label="验证码" required>
                            <n-input-group>
                                <n-input v-model:value="user.code" />
                                <n-button @click="sendVerificationCode" style="margin-bottom: 0" type="primary" ghost
                                    :disabled="verify_code_timeout > 0">
                                    {{ verify_code_timeout > 0 ? `等待${verify_code_timeout}秒` : "发送验证码" }}
                                </n-button>
                            </n-input-group>
                        </n-form-item-row>
                    </n-form>
                    <n-button @click="emailSignup" type="primary" block secondary strong>
                        注册
                    </n-button>
                </n-tab-pane>
            </n-tabs>
        </n-card>
        <n-modal v-model:show="showModal" style="max-width: 600px;" preset="card" title="重置密码">
            <n-form>
                <n-form-item-row label="邮箱" required>
                    <n-input v-model:value="user.email" />
                </n-form-item-row>
                <n-form-item-row label="新密码" required>
                    <n-input v-model:value="user.password" type="password" show-password-on="click" />
                </n-form-item-row>
                <div v-if="settings.cf_turnstile_site_key && !cf_turnstile_id">人机验证正在加载...</div>
                <div v-if="settings.cf_turnstile_site_key" id="cf-turnstile"></div>
                <n-form-item-row label="验证码" required>
                    <n-input-group>
                        <n-input v-model:value="user.code" />
                        <n-button @click="sendVerificationCode" style="margin-bottom: 0" type="primary" ghost
                            :disabled="verify_code_timeout > 0">
                            {{ verify_code_timeout > 0 ? `等待${verify_code_timeout}秒` : "发送验证码" }}
                        </n-button>
                    </n-input-group>
                </n-form-item-row>
            </n-form>
            <n-button @click="emailSignup" type="primary" block secondary strong>
                重置密码
            </n-button>
        </n-modal>
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
