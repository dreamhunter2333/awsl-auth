import { BrowserRouter, Route, Routes } from "react-router";
import { Toaster } from "@/components/ui/sonner"

import { LoginForm } from "@/components/login-form"
import { RegisterForm } from "@/components/register-form"
import { SiteHeader } from '@/components/site-header'
import { GlobalProvider } from "@/components/global-provider";
import { useTheme } from "@/components/theme-provider"
import { Callback } from "@/components/callback";
import { Demo } from "@/components/demo";


export default function App() {
  const { theme } = useTheme()
  return (
    <GlobalProvider>
      <div className="bg-muted w-full h-screen">
        <Toaster richColors position="top-center" theme={theme} />
        <SiteHeader />
        <div className="flex flex-col items-center justify-center gap-6 p-6 md:p-10">
          <div className="flex w-full max-w-md flex-col gap-6">
            <BrowserRouter>
              <Routes>
                <Route index element={<LoginForm />} />
                <Route path="/register" element={<RegisterForm />} />
                <Route path="/reset_pass" element={<RegisterForm ResetPass={true} />} />
                <Route path="/callback/:loginType" element={<Callback />} />
                <Route path="/demo" element={<Demo />} />
              </Routes>
            </BrowserRouter>
          </div>
        </div>
      </div>
    </GlobalProvider >
  )
}
