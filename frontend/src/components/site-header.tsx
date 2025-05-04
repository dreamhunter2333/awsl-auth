import { ModeSwitcher } from "@/components/mode-switcher";
import { Button } from "@/components//ui/button";
import { Icons } from "@/components//icons";


export function SiteHeader() {
    return (
        <header className="border-grid sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-16 items-center mx-auto sm:justify-between sm:space-x-0">
                <span className="inline-block font-bold">Awsl Auth</span>
                <div className="flex flex-1 items-center justify-end space-x-4">
                    <nav className="flex items-center space-x-1">
                        <Button
                            asChild
                            variant="ghost"
                            size="icon"
                            className="h-8 w-8 px-0"
                        >
                            <a
                                href="https://github.com/dreamhunter2333/awsl-auth"
                                target="_blank"
                                rel="noreferrer"
                            >
                                <Icons.github className="h-4 w-4" />
                                <span className="sr-only">GitHub</span>
                            </a>
                        </Button>
                        <ModeSwitcher />
                    </nav>
                </div>
            </div>
        </header>
    )
}
