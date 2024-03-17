import { ref } from "vue";
import { createGlobalState, useStorage, useSessionStorage } from '@vueuse/core'

export const useGlobalState = createGlobalState(
    () => {
        const loading = ref(false);
        const jwtSession = useSessionStorage('jwtSession', '');
        const themeSwitch = useStorage('themeSwitch', false);
        const appIdSession = useSessionStorage('appIdSession', 'demo');
        const settings = ref({
            enabled_smtp: false,
            enabled_github: false,
            enabled_google: false,
        });
        return {
            loading,
            settings,
            jwtSession,
            themeSwitch,
            appIdSession,
        }
    },
)
