import { toast } from 'vue-sonner';

export const showExperimentsToast = () => {
    toast.error('Navigation Error', {
        description: 'Unable to navigate to Brain Dump. If this issue continues, please contact support.',
        duration: 3000,
        position: 'bottom-right',
        style: {
            background: 'var(--element-color-1)',
            color: 'var(--light-text)',
            border: '1px solid var(--highlight-color)',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        },
    });
};