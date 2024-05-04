import { ref } from "vue";
import { createGlobalState, useStorage, useSessionStorage, useDark, useToggle } from '@vueuse/core'

export const useGlobalState = createGlobalState(
    () => {
        const loading = ref(false);
        const isDark = useDark()
        const toggleDark = useToggle(isDark)
        const jwtSession = useSessionStorage('jwtSession', '');
        const appIdSession = useSessionStorage('appIdSession', 'demo');
        const settings = ref({
            enabled_smtp: false,
            enabled_github: false,
            enabled_google: false,
            enabled_ms: false,
            enabled_web3: false,
            cf_turnstile_site_key: '',
        });
        return {
            loading,
            settings,
            jwtSession,
            isDark,
            toggleDark,
            appIdSession,
        }
    },
)
