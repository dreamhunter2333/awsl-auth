import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    InputOTP,
    InputOTPGroup,
    InputOTPSlot,
} from "@/components/ui/input-otp"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Link, useNavigate } from "react-router"
import { Turnstile } from '@marsidev/react-turnstile'
import { useState } from "react"
import { useTheme } from "@/components/theme-provider"
import { toast } from "sonner"
import { useGlobal } from "@/components/global-provider"
import { UseApiClient } from "@/api"
import { hashPassword } from "@/utils"
import { Eye, EyeClosed } from "lucide-react"

interface RegisterFormProps extends React.ComponentPropsWithoutRef<"div"> {
    ResetPass?: boolean
}


export function RegisterForm({
    className,
    ResetPass,
    ...props
}: RegisterFormProps) {
    const { theme } = useTheme()
    const { settings } = useGlobal()
    const { apiFetch } = UseApiClient()
    const navigate = useNavigate()
    const [token, setToken] = useState<string | null>(null)
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [showPassword, setShowPassword] = useState(false);
    const [code, setCode] = useState<string>("")
    const [verifyCodeTimeout, setVerifyCodeTimeout] = useState<number>(0)
    if (!settings.enabled_smtp) return null;
    const sendVerificationCode = async () => {
        if (!email) {
            toast.error("请输入邮箱");
            return;
        }
        if (!token && settings.cf_turnstile_site_key) {
            toast.error("请完成人机验证");
            return;
        }
        try {
            // const res = await apiFetch<{
            //     timeout: number
            // }>(`/api/email/verify_code`, {
            //     method: "POST",
            //     body: JSON.stringify({
            //         email: email,
            //         cf_token: token
            //     })
            // });
            const res = {
                timeout: 120
            }
            if (res && res.timeout) {
                toast.success(`验证码已发送, 有效期 ${res.timeout} 秒`);
                setVerifyCodeTimeout(res.timeout);
                const intervalId = setInterval(() => {
                    setVerifyCodeTimeout((prev) => {
                        if (prev <= 1) {
                            clearInterval(intervalId);
                            return 0;
                        }
                        return prev - 1;
                    });
                }, 1000);
            }
        } catch (error) {
            toast.error((error as Error).message || "发送验证码失败");
        }
    };

    const emailSignup = async () => {
        if (!email || !password || !code) {
            toast.error("请输入邮箱, 密码和验证码");
            return;
        }
        try {
            const res = await apiFetch(`/api/email/register`, {
                method: "POST",
                body: JSON.stringify({
                    email: email,
                    // hash password
                    password: await hashPassword(password),
                    code: code
                })
            });
            if (res) {
                toast.success("注册成功, 请登录");
                navigate("/");
            }
        } catch (error) {
            toast.error((error as Error).message || "注册失败");
        }
    };
    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Card>
                <CardHeader className="text-center">
                    <CardTitle className="text-xl">
                        {ResetPass ? "重置密码" : "注册"}
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-6">
                        <div className="grid gap-6">
                            <div className="grid gap-2">
                                <Label htmlFor="email">邮件</Label>
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
                                    <Label htmlFor="password">
                                        {ResetPass ? "新密码" : "密码"}
                                    </Label>
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
                            {settings.cf_turnstile_site_key && <div className="text-center">
                                <Turnstile
                                    siteKey={settings.cf_turnstile_site_key}
                                    options={{
                                        theme: theme,
                                        language: 'zh-CN',
                                    }}
                                    onSuccess={setToken} />
                            </div>}
                            <div className="grid grid-flow-col items-center gap-2">
                                <InputOTP maxLength={6}
                                    value={code}
                                    onChange={(e) => setCode(e)}
                                >
                                    <InputOTPGroup>
                                        <InputOTPSlot index={0} />
                                        <InputOTPSlot index={1} />
                                        <InputOTPSlot index={2} />
                                        <InputOTPSlot index={3} />
                                        <InputOTPSlot index={4} />
                                        <InputOTPSlot index={5} />
                                    </InputOTPGroup>
                                </InputOTP>
                                <Button variant="secondary"
                                    disabled={verifyCodeTimeout > 0}
                                    onClick={() => sendVerificationCode()}>
                                    {verifyCodeTimeout > 0 ? `等待${verifyCodeTimeout} 秒` : "发送验证码"}
                                </Button>
                            </div>
                            <Button className="w-full" onClick={() => emailSignup()}>
                                {ResetPass ? "重置密码" : "注册"}
                            </Button>
                            <Button variant="outline" asChild className="w-full">
                                <Link to="/">返回登录</Link>
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
