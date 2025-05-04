import { createContext, useContext, useEffect, useState } from "react"
import { FullScreenLoader } from "@/components/loading-spinner"
import { UseApiClient } from "@/api"
import { toast } from "sonner"


type GlobalProviderState = {
    isLoading: boolean
    setIsLoading: (isLoading: boolean) => void
    appIdSession: string
    setAppIdSession: (appId: string) => void
    jwtSession: string
    setJwtSession: (jwt: string) => void
    settings: GlobalSettings
}

const initialState: GlobalProviderState = {
    isLoading: false,
    setIsLoading: () => null,
    appIdSession: "demo",
    setAppIdSession: () => null,
    jwtSession: "",
    setJwtSession: () => null,
    settings: {} as GlobalSettings
}

type GlobalSettings = {
    fetched: boolean | undefined
    enabled_smtp: boolean | undefined
    enabled_github: boolean | undefined
    enabled_google: boolean | undefined
    enabled_ms: boolean | undefined
    enabled_web3: boolean | undefined
    cf_turnstile_site_key: string | undefined
}

const GlobalContext = createContext<GlobalProviderState>(initialState)

export function GlobalProvider(
    { children }: { children: React.ReactNode }
) {
    const { apiFetch } = UseApiClient()
    const [isLoading, setIsLoading] = useState(false);
    const [appIdSession, setAppIdSession] = useState<string>(
        () => (sessionStorage.getItem("appIdSession")) || "demo"
    )
    const [jwtSession, setJwtSession] = useState<string>(
        () => (sessionStorage.getItem("jwtSession")) || ""
    )
    const [settings, setSettings] = useState<GlobalSettings>({} as GlobalSettings)

    useEffect(() => {
        const fetchSettings = async () => {
            try {
                const settings_res = await apiFetch<GlobalSettings>('/api/settings');
                setSettings(settings_res);
            } catch (err) {
                toast.error((err as Error).message || "获取设置失败");
            } finally {
                setSettings((prev) => ({
                    ...prev,
                    fetched: true,
                }))
            }
        };

        fetchSettings();
    }, []);

    const value = {
        isLoading,
        setIsLoading,
        appIdSession,
        setAppIdSession: (appId: string) => {
            sessionStorage.setItem("appIdSession", appId)
            setAppIdSession(appId)
        },
        jwtSession,
        setJwtSession: (jwt: string) => {
            sessionStorage.setItem("jwtSession", jwt)
            setJwtSession(jwt)
        },
        settings,
    }

    return (
        <GlobalContext.Provider value={value}>
            <FullScreenLoader isLoading={isLoading} />
            {settings.fetched ? children : <FullScreenLoader isLoading={true} />}
        </GlobalContext.Provider>
    )
}

export const useGlobal = () => {
    return useContext(GlobalContext);
};
