<script setup>
import { NLayoutHeader, NButton, NIcon, NSwitch } from 'naive-ui'
import { DarkModeFilled, DarkModeOutlined, StarOutlineFilled } from '@vicons/material'

import { useGlobalState } from '../store'

const { themeSwitch } = useGlobalState()
</script>

<template>
    <n-layout-header>
        <h2 style="display: inline-block; margin-left: 10px;">AWSL</h2>
        <div>
            <n-switch v-model:value="themeSwitch" style="margin: 10px;">
                <template #checked-icon>
                    <n-icon :component="DarkModeFilled" />
                </template>
                <template #unchecked-icon>
                    <n-icon :component="DarkModeOutlined" />
                </template>
            </n-switch>
            <n-button style="margin: 10px;" tag="a" target="_blank" tertiary type="primary" round
                href="https://github.com/dreamhunter2333/cloudflare_temp_email">
                <n-icon :component="StarOutlineFilled" /> Github
            </n-button>
        </div>
    </n-layout-header>
</template>

<style scoped>
.n-layout-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
</style>
