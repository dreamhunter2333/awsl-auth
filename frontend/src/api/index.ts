import axios, { AxiosError } from 'axios'
import { useGlobal } from "@/components/global-provider";

const API_BASE = import.meta.env.VITE_API_BASE || "";

const instance = axios.create({
    baseURL: API_BASE,
    timeout: 10000
});

export function UseApiClient() {
    const { setIsLoading } = useGlobal();

    const apiFetch = async <T>(
        path: string,
        options: {
            method?: string,
            body?: string,
            headers?: unknown
        } = {}
    ): Promise<T> => {
        setIsLoading(true);
        try {
            const response = await instance.request<T>({
                url: path,
                method: options.method || 'GET',
                data: options.body || null,
                headers: options?.headers || {
                    'Content-Type': 'application/json',
                },
            });
            if (response.status >= 300) {
                throw new Error(`[Error]${response.status}: ${response.data}`);
            }
            const data = response.data;
            return data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const err = error as AxiosError;
                const detail = (err.response?.data as {
                    detail: string;
                })?.detail;
                throw new Error(`[Error]${err.status}: ${detail}`);
            } else {
                throw new Error(`[Error]: ${error}`);
            }
        } finally {
            setIsLoading(false);
        }
    }

    return {
        apiFetch
    }
}
