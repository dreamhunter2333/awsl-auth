import { cn } from "@/lib/utils";
import { Link, useSearchParams } from "react-router";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useGlobal } from "@/components/global-provider";
import { toast } from "sonner";
import { UseApiClient } from "@/api";

export function Demo({
    className,
    ...props
}: React.ComponentPropsWithoutRef<"div">) {
    const { apiFetch } = UseApiClient()
    const [URLSearchParams] = useSearchParams();
    const { jwtSession, setJwtSession, appIdSession } = useGlobal();
    const [user, setUser] = useState<Record<string, string>>({});
    useEffect(() => {
        const code = URLSearchParams.get("code");
        const fetchData = async () => {
            if (!code && !jwtSession) {
                return;
            }
            if (code) {
                try {
                    const { jwt } = await apiFetch<{
                        jwt: string;
                    }>("/api/token", {
                        method: "POST",
                        body: JSON.stringify({
                            app_id: appIdSession || "demo",
                            app_secret: "demo_secret",
                            code: code,
                        })
                    });
                    setJwtSession(jwt);
                } catch (error) {
                    toast.error((error as Error).message || "登录失败");
                    return;
                }
                window.location.href = "/demo";
                return;
            }
            try {
                const app_id = appIdSession || "demo";
                const user_res = await apiFetch<
                    Record<string, string>
                >(`/api/info?app_id=${app_id}`, {
                    headers: {
                        'Authorization': `Bearer ${jwtSession}`,
                        'Content-Type': 'application/json',
                    }
                });
                setUser(user_res);
            } catch (error) {
                toast.error((error as Error).message || "获取用户信息失败");
            }
        }
        fetchData();
    }, []);

    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Card>
                <CardHeader className="text-center">
                    <CardTitle className="text-xl">用户信息</CardTitle>
                </CardHeader>
                <CardContent>
                    {(user && Object.keys(user).length > 0) ?
                        (
                            <pre className="text-sm whitespace-pre-wrap break-all">{JSON.stringify(user, null, 2)}</pre>
                        ) : (
                            <p className="text-sm">您还没有登录</p>
                        )}
                    <Button variant="outline" asChild className="w-full mt-4">
                        <Link to="/">返回登录</Link>
                    </Button>
                </CardContent>
            </Card>
        </div>
    )
}
