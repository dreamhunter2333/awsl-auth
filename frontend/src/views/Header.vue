<script setup>
import { NLayoutHeader, NButton, NIcon, NPageHeader, NAvatar } from 'naive-ui'
import { DarkModeFilled, LightModeFilled, StarOutlineFilled } from '@vicons/material'
import { GithubAlt } from '@vicons/fa'

import { useGlobalState } from '../store'

const { isDark, toggleDark } = useGlobalState()
</script>

<template>
    <n-layout-header>
        <n-page-header>
            <template #title>
                <h4>AWSL</h4>
            </template>
            <template #avatar>
                <n-avatar style="margin-left: 10px;" src="/awsl.png" />
            </template>
            <template #extra>
                <n-button circle @click="toggleDark()">
                    <template #icon>
                        <n-icon :component="isDark ? LightModeFilled : DarkModeFilled" />
                    </template>
                </n-button>
                <n-button tertiary round tag="a" target="_blank" type="primary"
                    href="https://github.com/dreamhunter2333/awsl-auth">
                    <template #icon>
                        <n-icon :component="GithubAlt" />
                    </template>
                    Github
                </n-button>
            </template>
        </n-page-header>
    </n-layout-header>
</template>

<style scoped>
.n-button {
    margin-right: 10px;
}
</style>
