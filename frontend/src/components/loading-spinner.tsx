import { Loader, LucideProps } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useTheme } from "@/components/theme-provider"

export interface IProps extends LucideProps {
    className?: string;
}

export const LoadingSpinner = ({ className, ...props }: IProps) => {
    return <Loader className={cn('animate-spin', className)} {...props} />;
};

interface FullScreenLoaderProps {
    isLoading: boolean;
}

export const FullScreenLoader = ({
    isLoading
}: FullScreenLoaderProps) => {
    const { theme } = useTheme()
    if (!isLoading) return;
    const themebg = theme === 'dark' ? 'bg-black' : 'bg-white';
    return (
        <div className={`fixed inset-0 flex items-center justify-center ${themebg} opacity-50`}>
            <LoadingSpinner className="h-8 w-8" />
        </div>
    );
};
