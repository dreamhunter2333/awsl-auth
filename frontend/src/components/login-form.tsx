import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Icons } from "@/components/icons"
import { Link } from "react-router"
import { UseApiClient } from "@/api"
import { useState } from "react"
import { toast } from "sonner"
import { hashPassword } from "@/utils"
import { useNavigate } from "react-router";
import { Eye, EyeClosed } from "lucide-react"
import { useGlobal } from "@/components/global-provider"
import { LoginType } from "@/type"

export function LoginForm({
    className,
    ...props
}: React.ComponentPropsWithoutRef<"div">) {
    const { apiFetch } = UseApiClient()
    const navigate = useNavigate()
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [showPassword, setShowPassword] = useState(false);
    const { settings } = useGlobal();

    const onOauthLogin = async (logintype: LoginType) => {
        try {
            const response = await apiFetch<string>(
                `/api/login?login_type=${logintype}` +
                `&redirect_url=${window.location.origin}/callback/${logintype}`,
            );
            if (!response) {
                toast.error(`跳转失败 ${response}`);
                return;
            }
            window.location.href = response;
        } catch (error) {
            toast.error((error as Error).message || "登录失败");
        }
    };

    const isEnableWeb3 = settings.enabled_web3 && window.ethereum;
    const web3Login = async () => {
        if (!window.ethereum) return;
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        if (accounts.length <= 0) {
            toast.error("请安装 MetaMask");
            return;
        }
        const account = accounts[0];
        navigate(`/callback/web3?web3_account=${account}`);
    }

    const emailLogin = async () => {
        if (!email || !password) {
            toast.error("请输入邮箱和密码");
            return;
        }
        try {
            const res = await apiFetch<{
                code: string;
            }>(`/api/email/login`, {
                method: "POST",
                body: JSON.stringify({
                    email: email,
                    // hash password
                    password: await hashPassword(password)
                })
            });
            if (!res || !res.code) {
                toast.error("登录失败");
                return;
            }
            navigate(`/callback/email?code=${res.code}`);
        } catch (error) {
            toast.error((error as Error).message || "登录失败");
            console.error((error as Error).message || "登录失败");
        }
        return;
    };
    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Card>
                <CardHeader className="text-center">
                    <CardTitle className="text-xl">登录</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-6">
                        <div className="flex flex-col gap-4">
                            {settings.enabled_github && <Button variant="outline" className="w-full"
                                onClick={() => onOauthLogin("github")}>
                                <Icons.github />
                                Github 登录
                            </Button>}
                            {settings.enabled_google && <Button variant="outline" className="w-full"
                                onClick={() => onOauthLogin("google")}>
                                <Icons.google />
                                Google 登录
                            </Button>}
                            {settings.enabled_ms && <Button variant="outline" className="w-full"
                                onClick={() => onOauthLogin("ms")}>
                                <Icons.microsoft />
                                Microsoft 登录
                            </Button>}
                            {isEnableWeb3 && <Button variant="outline" className="w-full"
                                onClick={() => web3Login()}>
                                <Icons.metamask />
                                Metamask 登录
                            </Button>}
                        </div>
                        {settings.enabled_smtp &&
                            <div>
                                <div className="relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t after:border-border">
                                </div>
                                <div className="grid gap-6">
                                    <div className="grid gap-2">
                                        <Label htmlFor="email">邮箱</Label>
                                        <Input
                                            id="email"
                                            type="email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            placeholder="m@example.com"
                                        />
                                    </div>
                                    <div className="grid gap-2">
                                        <div className="flex items-center">
                                            <Label htmlFor="password" >密码</Label>
                                            <Link to="/reset_pass" className="ml-auto text-sm underline-offset-4 hover:underline">
                                                忘记密码?
                                            </Link>
                                        </div>
                                        <div className="flex w-full max-w-sm items-center space-x-2">
                                            <Input id="password" type={showPassword ? "text" : "password"}
                                                value={password}
                                                onChange={(e) => setPassword(e.target.value)}
                                            />
                                            <Button variant="ghost" size="icon" onClick={() => setShowPassword(!showPassword)} >
                                                {showPassword ? <Eye /> : <EyeClosed />}
                                            </Button>
                                        </div>

                                    </div>
                                    <Button className="w-full" onClick={() => emailLogin()}>
                                        登录
                                    </Button>
                                </div>
                                <div className="text-center text-sm">
                                    还没有账号?{" "}
                                    <Link to="/register" className="underline underline-offset-4">
                                        注册
                                    </Link>
                                </div>
                            </div>
                        }
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
