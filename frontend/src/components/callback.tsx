import { cn } from "@/lib/utils";
import { Link, useNavigate, useParams, useSearchParams } from "react-router";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useGlobal } from "@/components/global-provider";
import { toast } from "sonner";
import { UseApiClient } from "@/api";

export function Callback({
    className,
    ...props
}: React.ComponentPropsWithoutRef<"div">) {
    const { loginType } = useParams();
    const navigate = useNavigate()
    const { apiFetch } = UseApiClient()
    const [URLSearchParams] = useSearchParams();
    const { appIdSession } = useGlobal();
    const [failed, setFailed] = useState(false);
    useEffect(() => {
        if (!loginType) {
            setFailed(true);
            toast.error(`登录失败 ${loginType}`);
            return;
        }
        const reqBody = {
            app_id: appIdSession || "demo",
            login_type: loginType,
            code: URLSearchParams.get("code"),
            web3_account: URLSearchParams.get("web3_account"),
            redirect_url: `${window.location.origin}${window.location.pathname}`
        };
        const loginApiCall = async () => {
            try {
                const response = await apiFetch<{
                    code: string;
                    redirect_url: string;
                }>(`/api/oauth`, {
                    method: "POST",
                    body: JSON.stringify(reqBody)
                });
                if (!response) {
                    setFailed(true);
                    toast.error(`登录失败 ${response}`);
                    return;
                }
                const { code, redirect_url } = response;
                if (!code) {
                    setFailed(true);
                    toast.error(`登录失败 ${response}`);
                    return;
                }
                if (redirect_url) {
                    const url = new URL(redirect_url);
                    url.searchParams.set("code", code);
                    window.location.href = url.href;
                    return;
                }
                navigate(`/demo?code=${code}`);
            } catch (error) {
                setFailed(true);
                toast.error(`登录失败 ${(error as Error).message}`);
                return;
            }
        }
        loginApiCall();
    }, []);

    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Card>
                <CardHeader className="text-center">
                    <CardTitle className="text-xl">登录中</CardTitle>
                </CardHeader>
                <CardContent>
                    {failed ? (
                        <div className="flex flex-col items-center justify-center gap-2">
                            <p className="text-sm text-red-500">
                                登录失败，请重试
                            </p>
                            <Button variant="outline" asChild className="w-full">
                                <Link to="/">返回登录</Link>
                            </Button>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center gap-2">
                            <p className="text-sm text-muted-foreground">
                                正在通过 {loginType} 登录中...
                            </p>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    )
}
