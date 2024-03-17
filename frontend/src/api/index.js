import axios from 'axios'
import { useGlobalState } from '../store'

const API_BASE = import.meta.env.VITE_API_BASE || "";
const { loading } = useGlobalState();

const instance = axios.create({
    baseURL: API_BASE,
    timeout: 10000
});

const apiFetch = async (path, options = {}) => {
    loading.value = true;
    try {
        const response = await instance.request(path, {
            method: options.method || 'GET',
            data: options.body || null,
            headers: options && options.headers ? options.headers : {
                'Content-Type': 'application/json',
            },
        });
        // if (response.status === 401 && openSettings.value.auth) {
        //     throw new Error("Unauthorized, you password is wrong")
        // }
        // if (response.status === 401 && path.startsWith("/admin")) {
        //     throw new Error("Unauthorized, you admin password is wrong")
        // }
        if (response.status >= 300) {
            throw new Error(`${response.status} ${response.data}` || "error");
        }
        const data = response.data;
        return data;
    } finally {
        loading.value = false;
    }
}

const getOpenSettings = async (message) => {
    try {
        const res = await api.fetch("/open_api/settings");
        openSettings.value = {
            prefix: res["prefix"] || "",
            needAuth: res["needAuth"] || false,
            domains: res["domains"].map((domain) => {
                return {
                    label: domain,
                    value: domain
                }
            })
        };
        if (openSettings.value.needAuth) {
            showAuth.value = true;
        }
    } catch (error) {
        message.error(error.message || "error");
    }
}

const getSettings = async () => {
    if (typeof jwt.value != 'string' || jwt.value.trim() === '' || jwt.value === 'undefined') {
        return "";
    }
    const res = await apiFetch("/api/settings");;
    settings.value = {
        address: res["address"],
        auto_reply: res["auto_reply"]
    };
}


export const api = {
    fetch: apiFetch,
    getSettings: getSettings,
    getOpenSettings: getOpenSettings
}
